import os
import gc
import json
import uuid
from pathlib import Path

import torch
import gradio as gr
from PIL import Image
from diffusers import (
    StableDiffusionXLPipeline,
    StableDiffusionXLImg2ImgPipeline,
    StableDiffusionXLInpaintPipeline,
)

# =========================
# Config
# =========================
BASE_MODEL = "stabilityai/stable-diffusion-xl-base-1.0"

OUTPUT_DIR = Path("/kaggle/working/visualforge_outputs")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

METADATA_PATH = OUTPUT_DIR / "metadata.jsonl"

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
DTYPE = torch.float16 if DEVICE == "cuda" else torch.float32


def find_lora_file(filename):
    matches = list(Path("/kaggle/input").rglob(filename))
    return matches[0] if matches else None


PRODUCT_LORA_FILE = find_lora_file("product_ads_lora_300.safetensors")
EGYPTIAN_LORA_FILE = find_lora_file("pytorch_lora_weights_500.safetensors")


DOMAIN_CONFIG = {
    "base": {
        "label": "General / Base",
        "style_prefix": "",
        "adapter": None,
        "weight": None,
        "lora_file": None,
    },
    "product_ads": {
        "label": "Product Ads",
        "style_prefix": (
            "vforge_product_ad_style, professional product advertisement, premium commercial style, "
            "clean composition, studio lighting, glossy product photography, luxury branding look"
        ),
        "adapter": "product_ads",
        "weight": 0.45,
        "lora_file": PRODUCT_LORA_FILE,
    },
    "egyptian_cultural": {
        "label": "Egyptian Cultural",
        "style_prefix": (
            "vforge_egyptian_cultural_style, egyptian cultural style, heritage inspired visual design, "
            "ancient egyptian motifs, warm cinematic lighting, authentic cultural atmosphere"
        ),
        "adapter": "egyptian_cultural",
        "weight": 0.75,
        "lora_file": EGYPTIAN_LORA_FILE,
    },
}

PIPELINE_CLASSES = {
    "text2img": StableDiffusionXLPipeline,
    "img2img": StableDiffusionXLImg2ImgPipeline,
    "inpaint": StableDiffusionXLInpaintPipeline,
}

DEFAULT_NEGATIVE = (
    "low quality, blurry, soft focus, distorted, deformed, ugly, bad anatomy, "
    "bad composition, watermark, text, logo, messy background, extra objects"
)

_current_pipe = None
_current_mode = None


# =========================
# Memory helpers
# =========================
def clear_cuda():
    gc.collect()
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
        try:
            torch.cuda.ipc_collect()
        except Exception:
            pass


def cleanup():
    global _current_pipe, _current_mode

    if _current_pipe is not None:
        del _current_pipe

    _current_pipe = None
    _current_mode = None

    clear_cuda()


def normalize_dim(x, minimum=512, maximum=1024):
    x = int(x)
    x = max(minimum, min(maximum, x))
    x = (x // 8) * 8
    return x


# =========================
# Prompt + LoRA
# =========================
def build_prompt(prompt, domain):
    prompt = (prompt or "").strip()
    prefix = DOMAIN_CONFIG[domain]["style_prefix"].strip()

    if prefix:
        return f"{prefix}, {prompt}"
    return prompt


def load_loras(pipe):
    loaded = []

    if PRODUCT_LORA_FILE is not None:
        pipe.load_lora_weights(
            str(PRODUCT_LORA_FILE.parent),
            weight_name=PRODUCT_LORA_FILE.name,
            adapter_name="product_ads",
        )
        loaded.append("product_ads")

    if EGYPTIAN_LORA_FILE is not None:
        pipe.load_lora_weights(
            str(EGYPTIAN_LORA_FILE.parent),
            weight_name=EGYPTIAN_LORA_FILE.name,
            adapter_name="egyptian_cultural",
        )
        loaded.append("egyptian_cultural")

    pipe._visualforge_loaded_loras = loaded
    return pipe


def apply_domain(pipe, domain):
    cfg = DOMAIN_CONFIG[domain]
    adapter = cfg["adapter"]
    weight = cfg["weight"]
    lora_file = cfg["lora_file"]

    if adapter is None:
        try:
            pipe.disable_lora()
        except Exception:
            pass
        return pipe, "No LoRA - Base SDXL"

    if lora_file is None:
        try:
            pipe.disable_lora()
        except Exception:
            pass
        return pipe, f"LoRA file not found for {domain}; using prompt style only"

    try:
        pipe.enable_lora()
        pipe.set_adapters([adapter], adapter_weights=[float(weight)])
        return pipe, f"LoRA active: {adapter} | weight={weight}"
    except Exception as e:
        try:
            pipe.disable_lora()
        except Exception:
            pass
        return pipe, f"LoRA failed for {adapter}: {e}"


# =========================
# Pipeline loading
# =========================
def load_pipe(mode):
    global _current_pipe, _current_mode

    if mode not in PIPELINE_CLASSES:
        raise ValueError(f"Unknown mode: {mode}")

    if _current_pipe is not None and _current_mode == mode:
        return _current_pipe

    cleanup()

    pipe_cls = PIPELINE_CLASSES[mode]

    kwargs = {
        "torch_dtype": DTYPE,
        "use_safetensors": True,
    }

    if DEVICE == "cuda":
        kwargs["variant"] = "fp16"

    pipe = pipe_cls.from_pretrained(BASE_MODEL, **kwargs)

    if DEVICE == "cuda":
        pipe = pipe.to("cuda")
    else:
        pipe = pipe.to("cpu")

    if hasattr(pipe, "enable_attention_slicing"):
        pipe.enable_attention_slicing()

    if hasattr(pipe, "enable_vae_slicing"):
        pipe.enable_vae_slicing()

    if hasattr(pipe, "enable_vae_tiling"):
        pipe.enable_vae_tiling()

    pipe = load_loras(pipe)

    _current_pipe = pipe
    _current_mode = mode

    return pipe


# =========================
# Save helpers
# =========================
def save_image_and_metadata(image, metadata):
    image_id = uuid.uuid4().hex[:8]
    filename = f"{metadata['mode']}_{metadata['domain']}_{image_id}.png"
    output_path = OUTPUT_DIR / filename

    image.save(output_path)

    record = {
        "image_path": str(output_path),
        **metadata,
    }

    with open(METADATA_PATH, "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")

    return str(output_path), record


def build_status_text(record):
    lines = [
        f"Saved: {record['image_path']}",
        f"Mode: {record['mode']}",
        f"Domain: {record['domain']}",
        f"LoRA Status: {record.get('lora_status', 'N/A')}",
        f"Seed: {record['seed']}",
        f"Steps: {record['steps']}",
        f"Guidance: {record['guidance_scale']}",
        f"Size: {record['width']}x{record['height']}",
    ]

    if "strength" in record:
        lines.append(f"Strength: {record['strength']}")

    return "\n".join(lines)


def get_gallery_items():
    images = sorted(OUTPUT_DIR.glob("*.png"), key=lambda p: p.stat().st_mtime, reverse=True)
    return [(str(p), p.name) for p in images]


def get_metadata_text():
    if not METADATA_PATH.exists():
        return "No metadata yet."

    lines = []
    with open(METADATA_PATH, "r", encoding="utf-8") as f:
        for line in f.readlines()[-10:]:
            try:
                item = json.loads(line)
                lines.append(
                    f"{Path(item['image_path']).name} | "
                    f"mode={item.get('mode')} | "
                    f"domain={item.get('domain')} | "
                    f"lora={item.get('lora_status')}"
                )
            except Exception:
                pass

    return "\n".join(lines) if lines else "No metadata yet."


# =========================
# Core generation functions
# =========================
def generate_text(
    prompt,
    domain,
    seed,
    steps,
    guidance_scale,
    width,
    height,
    negative_prompt,
):
    if not prompt or not prompt.strip():
        raise gr.Error("Please enter a prompt.")

    width = normalize_dim(width)
    height = normalize_dim(height)

    pipe = load_pipe("text2img")
    pipe, lora_status = apply_domain(pipe, domain)

    final_prompt = build_prompt(prompt, domain)
    generator = torch.Generator(device=DEVICE).manual_seed(int(seed))

    image = pipe(
        prompt=final_prompt,
        negative_prompt=negative_prompt or DEFAULT_NEGATIVE,
        num_inference_steps=int(steps),
        guidance_scale=float(guidance_scale),
        width=width,
        height=height,
        generator=generator,
    ).images[0]

    _, record = save_image_and_metadata(
        image,
        {
            "mode": "text2img",
            "domain": domain,
            "prompt": final_prompt,
            "lora_status": lora_status,
            "seed": int(seed),
            "steps": int(steps),
            "guidance_scale": float(guidance_scale),
            "width": width,
            "height": height,
        },
    )

    return image, final_prompt, build_status_text(record), get_gallery_items(), get_metadata_text()


def generate_img2img(
    input_image,
    prompt,
    domain,
    seed,
    steps,
    guidance_scale,
    strength,
    width,
    height,
    negative_prompt,
):
    if input_image is None:
        raise gr.Error("Please upload a source image.")

    if not prompt or not prompt.strip():
        raise gr.Error("Please enter a prompt.")

    width = normalize_dim(width)
    height = normalize_dim(height)

    pipe = load_pipe("img2img")
    pipe, lora_status = apply_domain(pipe, domain)

    final_prompt = build_prompt(prompt, domain)
    input_image = input_image.convert("RGB").resize((width, height))
    generator = torch.Generator(device=DEVICE).manual_seed(int(seed))

    image = pipe(
        prompt=final_prompt,
        image=input_image,
        negative_prompt=negative_prompt or DEFAULT_NEGATIVE,
        num_inference_steps=int(steps),
        guidance_scale=float(guidance_scale),
        strength=float(strength),
        generator=generator,
    ).images[0]

    _, record = save_image_and_metadata(
        image,
        {
            "mode": "img2img",
            "domain": domain,
            "prompt": final_prompt,
            "lora_status": lora_status,
            "seed": int(seed),
            "steps": int(steps),
            "guidance_scale": float(guidance_scale),
            "strength": float(strength),
            "width": width,
            "height": height,
        },
    )

    return image, final_prompt, build_status_text(record), get_gallery_items(), get_metadata_text()


def generate_inpaint(
    input_image,
    mask_image,
    prompt,
    domain,
    seed,
    steps,
    guidance_scale,
    strength,
    width,
    height,
    negative_prompt,
):
    if input_image is None:
        raise gr.Error("Please upload a source image.")

    if mask_image is None:
        raise gr.Error("Please upload a mask image.")

    if not prompt or not prompt.strip():
        raise gr.Error("Please enter a prompt.")

    width = normalize_dim(width)
    height = normalize_dim(height)

    pipe = load_pipe("inpaint")
    pipe, lora_status = apply_domain(pipe, domain)

    final_prompt = build_prompt(prompt, domain)

    input_image = input_image.convert("RGB").resize((width, height))
    mask_image = mask_image.convert("L").resize((width, height))
    generator = torch.Generator(device=DEVICE).manual_seed(int(seed))

    image = pipe(
        prompt=final_prompt,
        image=input_image,
        mask_image=mask_image,
        negative_prompt=negative_prompt or DEFAULT_NEGATIVE,
        num_inference_steps=int(steps),
        guidance_scale=float(guidance_scale),
        strength=float(strength),
        generator=generator,
    ).images[0]

    _, record = save_image_and_metadata(
        image,
        {
            "mode": "inpaint",
            "domain": domain,
            "prompt": final_prompt,
            "lora_status": lora_status,
            "seed": int(seed),
            "steps": int(steps),
            "guidance_scale": float(guidance_scale),
            "strength": float(strength),
            "width": width,
            "height": height,
        },
    )

    return image, final_prompt, build_status_text(record), get_gallery_items(), get_metadata_text()


# =========================
# Health info
# =========================
def health_text():
    gpu_name = torch.cuda.get_device_name(0) if torch.cuda.is_available() else "CPU"

    return (
        f"Device: {DEVICE}\n"
        f"GPU: {gpu_name}\n"
        f"Base Model: {BASE_MODEL}\n"
        f"Product Ads LoRA: {PRODUCT_LORA_FILE if PRODUCT_LORA_FILE else 'NOT FOUND'}\n"
        f"Egyptian Cultural LoRA: {EGYPTIAN_LORA_FILE if EGYPTIAN_LORA_FILE else 'NOT FOUND'}\n"
        f"Output Dir: {OUTPUT_DIR}"
    )


def refresh_gallery():
    return get_gallery_items(), get_metadata_text()


# =========================
# UI
# =========================
with gr.Blocks(theme=gr.themes.Soft(), title="VisualForge AI") as demo:
    gr.Markdown("# VisualForge AI")
    gr.Markdown(
        "Real SDXL running on Kaggle GPU with Product Ads LoRA and Egyptian Cultural LoRA."
    )

    system_status = gr.Textbox(
        value=health_text(),
        label="System Status",
        interactive=False,
        lines=7,
    )

    with gr.Tabs():
        # =========================
        # Text-to-Image
        # =========================
        with gr.Tab("Text-to-Image"):
            with gr.Row():
                with gr.Column(scale=1):
                    txt_prompt = gr.Textbox(
                        label="Prompt",
                        lines=4,
                        value="A modern perfume bottle on a dark futuristic background, cinematic lighting, high quality",
                    )

                    txt_domain = gr.Dropdown(
                        choices=[
                            ("General / Base", "base"),
                            ("Product Ads", "product_ads"),
                            ("Egyptian Cultural", "egyptian_cultural"),
                        ],
                        value="base",
                        label="Domain",
                    )

                    txt_negative = gr.Textbox(
                        label="Negative Prompt",
                        lines=2,
                        value=DEFAULT_NEGATIVE,
                    )

                    with gr.Row():
                        txt_seed = gr.Number(value=42, label="Seed", precision=0)
                        txt_steps = gr.Slider(5, 40, value=20, step=1, label="Steps")
                        txt_guidance = gr.Slider(1, 15, value=7.5, step=0.5, label="Guidance")

                    with gr.Row():
                        txt_width = gr.Dropdown([512, 768, 1024], value=768, label="Width")
                        txt_height = gr.Dropdown([512, 768, 1024], value=768, label="Height")

                    txt_btn = gr.Button("Generate Text-to-Image", variant="primary")

                with gr.Column(scale=1):
                    txt_output = gr.Image(label="Generated Image", type="pil")
                    txt_final_prompt = gr.Textbox(label="Final Prompt", lines=4, interactive=False)
                    txt_status = gr.Textbox(label="Status", lines=8, interactive=False)

        # =========================
        # Image-to-Image
        # =========================
        with gr.Tab("Image-to-Image"):
            with gr.Row():
                with gr.Column(scale=1):
                    img_input = gr.Image(label="Source Image", type="pil")
                    img_prompt = gr.Textbox(
                        label="Prompt",
                        lines=4,
                        value="Transform this image into a professional product advertisement",
                    )

                    img_domain = gr.Dropdown(
                        choices=[
                            ("General / Base", "base"),
                            ("Product Ads", "product_ads"),
                            ("Egyptian Cultural", "egyptian_cultural"),
                        ],
                        value="product_ads",
                        label="Domain",
                    )

                    img_negative = gr.Textbox(
                        label="Negative Prompt",
                        lines=2,
                        value=DEFAULT_NEGATIVE,
                    )

                    with gr.Row():
                        img_seed = gr.Number(value=123, label="Seed", precision=0)
                        img_steps = gr.Slider(5, 40, value=20, step=1, label="Steps")
                        img_guidance = gr.Slider(1, 15, value=7.5, step=0.5, label="Guidance")

                    with gr.Row():
                        img_strength = gr.Slider(0.1, 1.0, value=0.35, step=0.05, label="Strength")
                        img_width = gr.Dropdown([512, 768, 1024], value=768, label="Width")
                        img_height = gr.Dropdown([512, 768, 1024], value=768, label="Height")

                    img_btn = gr.Button("Generate Image-to-Image", variant="primary")

                with gr.Column(scale=1):
                    img_output = gr.Image(label="Generated Image", type="pil")
                    img_final_prompt = gr.Textbox(label="Final Prompt", lines=4, interactive=False)
                    img_status = gr.Textbox(label="Status", lines=8, interactive=False)

        # =========================
        # Inpainting
        # =========================
        with gr.Tab("Inpainting"):
            with gr.Row():
                with gr.Column(scale=1):
                    inpaint_input = gr.Image(label="Source Image", type="pil")
                    inpaint_mask = gr.Image(label="Mask Image", type="pil")

                    inpaint_prompt = gr.Textbox(
                        label="Prompt",
                        lines=4,
                        value="Replace the selected area with a glowing futuristic background",
                    )

                    inpaint_domain = gr.Dropdown(
                        choices=[
                            ("General / Base", "base"),
                            ("Product Ads", "product_ads"),
                            ("Egyptian Cultural", "egyptian_cultural"),
                        ],
                        value="egyptian_cultural",
                        label="Domain",
                    )

                    inpaint_negative = gr.Textbox(
                        label="Negative Prompt",
                        lines=2,
                        value=DEFAULT_NEGATIVE,
                    )

                    with gr.Row():
                        inpaint_seed = gr.Number(value=777, label="Seed", precision=0)
                        inpaint_steps = gr.Slider(5, 40, value=20, step=1, label="Steps")
                        inpaint_guidance = gr.Slider(1, 15, value=7.5, step=0.5, label="Guidance")

                    with gr.Row():
                        inpaint_strength = gr.Slider(0.1, 1.0, value=0.45, step=0.05, label="Strength")
                        inpaint_width = gr.Dropdown([512, 768, 1024], value=768, label="Width")
                        inpaint_height = gr.Dropdown([512, 768, 1024], value=768, label="Height")

                    inpaint_btn = gr.Button("Generate Inpainting", variant="primary")

                with gr.Column(scale=1):
                    inpaint_output = gr.Image(label="Generated Image", type="pil")
                    inpaint_final_prompt = gr.Textbox(label="Final Prompt", lines=4, interactive=False)
                    inpaint_status = gr.Textbox(label="Status", lines=8, interactive=False)

        # =========================
        # Gallery
        # =========================
        with gr.Tab("Gallery"):
            refresh_btn = gr.Button("Refresh Gallery")
            gallery = gr.Gallery(
                label="Saved Outputs",
                value=get_gallery_items(),
                columns=3,
                height=500,
            )
            metadata_box = gr.Textbox(
                label="Recent Metadata",
                value=get_metadata_text(),
                lines=12,
                interactive=False,
            )

    txt_btn.click(
        fn=generate_text,
        inputs=[
            txt_prompt,
            txt_domain,
            txt_seed,
            txt_steps,
            txt_guidance,
            txt_width,
            txt_height,
            txt_negative,
        ],
        outputs=[txt_output, txt_final_prompt, txt_status, gallery, metadata_box],
    )

    img_btn.click(
        fn=generate_img2img,
        inputs=[
            img_input,
            img_prompt,
            img_domain,
            img_seed,
            img_steps,
            img_guidance,
            img_strength,
            img_width,
            img_height,
            img_negative,
        ],
        outputs=[img_output, img_final_prompt, img_status, gallery, metadata_box],
    )

    inpaint_btn.click(
        fn=generate_inpaint,
        inputs=[
            inpaint_input,
            inpaint_mask,
            inpaint_prompt,
            inpaint_domain,
            inpaint_seed,
            inpaint_steps,
            inpaint_guidance,
            inpaint_strength,
            inpaint_width,
            inpaint_height,
            inpaint_negative,
        ],
        outputs=[inpaint_output, inpaint_final_prompt, inpaint_status, gallery, metadata_box],
    )

    refresh_btn.click(
        fn=refresh_gallery,
        inputs=[],
        outputs=[gallery, metadata_box],
    )

demo.launch(share=True, debug=True)