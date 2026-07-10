import os
import gc
import json
import uuid
import torch
from PIL import Image
from diffusers import (
    StableDiffusionPipeline,
    StableDiffusionImg2ImgPipeline,
    StableDiffusionInpaintPipeline,
)

TEXT2IMG_MODEL = os.getenv(
    "VISUALFORGE_TEXT2IMG_MODEL",
    "runwayml/stable-diffusion-v1-5"
)

IMG2IMG_MODEL = os.getenv(
    "VISUALFORGE_IMG2IMG_MODEL",
    "runwayml/stable-diffusion-v1-5"
)

INPAINT_MODEL = os.getenv(
    "VISUALFORGE_INPAINT_MODEL",
    "runwayml/stable-diffusion-inpainting"
)

EGYPTIAN_LORA_DIR = os.getenv("EGYPTIAN_LORA_DIR", "")
PRODUCT_LORA_DIR = os.getenv("PRODUCT_LORA_DIR", "")

OUTPUT_DIR = os.getenv(
    "VISUALFORGE_OUTPUT_DIR",
    "C:/VF/visualforge-ai/backend/app/storage/outputs"
)

os.makedirs(OUTPUT_DIR, exist_ok=True)

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
DTYPE = torch.float16 if DEVICE == "cuda" else torch.float32

DOMAIN_CONFIG = {
    "base": {
        "trigger": "",
    },
    "product_ads": {
        "trigger": "professional product advertisement, premium commercial style, studio lighting, clean composition",
    },
    "egyptian_cultural": {
        "trigger": "egyptian cultural style, heritage inspired details, traditional motifs, cinematic composition",
    },
}

PIPELINE_CONFIG = {
    "text2img": {
        "class": StableDiffusionPipeline,
        "model_id": TEXT2IMG_MODEL,
    },
    "img2img": {
        "class": StableDiffusionImg2ImgPipeline,
        "model_id": IMG2IMG_MODEL,
    },
    "inpaint": {
        "class": StableDiffusionInpaintPipeline,
        "model_id": INPAINT_MODEL,
    },
}

DEFAULT_NEGATIVE = (
    "low quality, blurry, soft focus, distorted, deformed, ugly, bad composition, "
    "watermark, messy background, extra objects"
)

_current_pipe = None
_current_mode = None


def _cleanup():
    global _current_pipe, _current_mode

    if _current_pipe is not None:
        del _current_pipe

    _current_pipe = None
    _current_mode = None

    gc.collect()
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
        torch.cuda.ipc_collect()


def _validate_domain(domain):
    if domain not in DOMAIN_CONFIG:
        raise ValueError("Unknown domain. Use: base, product_ads, egyptian_cultural")


def _build_prompt(prompt, domain):
    trigger = DOMAIN_CONFIG[domain]["trigger"].strip()
    prompt = prompt.strip()
    return f"{trigger}, {prompt}" if trigger else prompt


def _apply_memory_optimizations(pipe):
    try:
        pipe.safety_checker = None
    except Exception:
        pass

    try:
        pipe.enable_attention_slicing()
    except Exception:
        pass

    try:
        pipe.enable_vae_slicing()
    except Exception:
        pass

    try:
        pipe.enable_vae_tiling()
    except Exception:
        pass

    try:
        pipe.enable_xformers_memory_efficient_attention()
    except Exception:
        pass

    if DEVICE == "cuda":
        pipe.enable_sequential_cpu_offload()
    else:
        pipe = pipe.to(DEVICE)

    return pipe


def _load_pipe(mode, domain):
    global _current_pipe, _current_mode

    if mode not in PIPELINE_CONFIG:
        raise ValueError(f"Unknown mode '{mode}'")

    _validate_domain(domain)

    if _current_pipe is not None and _current_mode == mode:
        return _current_pipe

    _cleanup()

    pipe_cls = PIPELINE_CONFIG[mode]["class"]
    model_id = PIPELINE_CONFIG[mode]["model_id"]

    pipe = pipe_cls.from_pretrained(
        model_id,
        torch_dtype=DTYPE,
        use_safetensors=True,
    )

    pipe = _apply_memory_optimizations(pipe)

    _current_pipe = pipe
    _current_mode = mode

    return pipe


def _save_image_and_metadata(image, metadata):
    image_id = str(uuid.uuid4())[:8]
    filename = f"{metadata['mode']}_{metadata['domain']}_{image_id}.png"
    output_path = os.path.join(OUTPUT_DIR, filename)

    image.save(output_path)

    record = {
        "image_path": output_path,
        **metadata,
    }

    metadata_path = os.path.join(OUTPUT_DIR, "api_metadata.jsonl")
    with open(metadata_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")

    return {
        "success": True,
        "image_path": output_path,
        "metadata": record,
    }


def text_to_image(
    prompt,
    domain="base",
    seed=42,
    steps=10,
    guidance_scale=7.5,
    width=512,
    height=512,
    negative_prompt=DEFAULT_NEGATIVE,
):
    pipe = _load_pipe("text2img", domain)
    final_prompt = _build_prompt(prompt, domain)

    generator = torch.Generator(device=DEVICE).manual_seed(int(seed))

    image = pipe(
        prompt=final_prompt,
        negative_prompt=negative_prompt,
        num_inference_steps=int(steps),
        guidance_scale=float(guidance_scale),
        width=int(width),
        height=int(height),
        generator=generator,
    ).images[0]

    return _save_image_and_metadata(
        image,
        {
            "mode": "text2img",
            "domain": domain,
            "prompt": final_prompt,
            "seed": seed,
            "steps": steps,
            "guidance_scale": guidance_scale,
            "width": width,
            "height": height,
        },
    )


def image_to_image(
    input_image_path,
    prompt,
    domain="base",
    seed=123,
    steps=10,
    guidance_scale=7.5,
    strength=0.35,
    width=512,
    height=512,
    negative_prompt=DEFAULT_NEGATIVE,
):
    pipe = _load_pipe("img2img", domain)
    final_prompt = _build_prompt(prompt, domain)

    input_image = Image.open(input_image_path).convert("RGB").resize((int(width), int(height)))
    generator = torch.Generator(device=DEVICE).manual_seed(int(seed))

    image = pipe(
        prompt=final_prompt,
        image=input_image,
        negative_prompt=negative_prompt,
        num_inference_steps=int(steps),
        guidance_scale=float(guidance_scale),
        strength=float(strength),
        generator=generator,
    ).images[0]

    return _save_image_and_metadata(
        image,
        {
            "mode": "img2img",
            "domain": domain,
            "prompt": final_prompt,
            "input_image": input_image_path,
            "seed": seed,
            "steps": steps,
            "guidance_scale": guidance_scale,
            "strength": strength,
            "width": width,
            "height": height,
        },
    )


def inpaint(
    input_image_path,
    mask_image_path,
    prompt,
    domain="base",
    seed=777,
    steps=10,
    guidance_scale=7.5,
    strength=0.45,
    width=512,
    height=512,
    negative_prompt=DEFAULT_NEGATIVE,
):
    pipe = _load_pipe("inpaint", domain)
    final_prompt = _build_prompt(prompt, domain)

    input_image = Image.open(input_image_path).convert("RGB").resize((int(width), int(height)))
    mask_image = Image.open(mask_image_path).convert("L").resize((int(width), int(height)))
    generator = torch.Generator(device=DEVICE).manual_seed(int(seed))

    image = pipe(
        prompt=final_prompt,
        image=input_image,
        mask_image=mask_image,
        negative_prompt=negative_prompt,
        num_inference_steps=int(steps),
        guidance_scale=float(guidance_scale),
        strength=float(strength),
        generator=generator,
    ).images[0]

    return _save_image_and_metadata(
        image,
        {
            "mode": "inpaint",
            "domain": domain,
            "prompt": final_prompt,
            "input_image": input_image_path,
            "mask_image": mask_image_path,
            "seed": seed,
            "steps": steps,
            "guidance_scale": guidance_scale,
            "strength": strength,
            "width": width,
            "height": height,
        },
    )


def health():
    def _exists(path_value):
        if not path_value:
            return False
        return os.path.exists(os.path.join(path_value, "pytorch_lora_weights.safetensors"))

    return {
        "status": "ready",
        "device": DEVICE,
        "base_model": TEXT2IMG_MODEL,
        "domains": list(DOMAIN_CONFIG.keys()),
        "output_dir": OUTPUT_DIR,
        "egyptian_lora_exists": _exists(EGYPTIAN_LORA_DIR),
        "product_ads_lora_exists": _exists(PRODUCT_LORA_DIR),
    }