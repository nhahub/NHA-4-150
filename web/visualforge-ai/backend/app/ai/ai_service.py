import importlib
from pathlib import Path
from typing import Any
from urllib.parse import quote

from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.modules.generations import service as generation_service
from app.modules.uploads.models import UploadedFile


ENGINE_MODE_BY_APP_MODE = {
    "text_to_image": "text2img",
    "image_to_image": "img2img",
    "inpainting": "inpaint",
}


def _load_engine():
    settings = get_settings()
    settings.sync_ai_environment()
    return importlib.import_module("app.ai.visualforge_engine")


def _public_url(path: str | None, mount_name: str) -> str | None:
    if not path:
        return None
    settings = get_settings()
    return f"{settings.API_BASE_URL.rstrip('/')}/{mount_name}/{quote(Path(path).name)}"


def output_url(path: str | None) -> str | None:
    return _public_url(path, "outputs")


def upload_url(path: str | None) -> str | None:
    return _public_url(path, "uploads")


def get_ai_health() -> dict[str, Any]:
    try:
        engine = _load_engine()
        health = engine.health()
        return {
            "status": health.get("status", "ready"),
            "device": health.get("device"),
            "base_model": health.get("base_model"),
            "domains": health.get("domains", []),
            "output_dir": str(get_settings().output_dir_path),
            "egyptian_lora_exists": health.get("egyptian_lora_exists", False),
            "product_ads_lora_exists": health.get("product_ads_lora_exists", False),
        }
    except Exception as exc:
        return {
            "status": "unavailable",
            "error": str(exc),
            "output_dir": str(get_settings().output_dir_path),
        }


def _engine_kwargs(
    *,
    prompt: str,
    domain: str,
    seed: int,
    steps: int,
    guidance_scale: float,
    width: int,
    height: int,
    strength: float | None = None,
    negative_prompt: str | None = None,
) -> dict[str, Any]:
    kwargs: dict[str, Any] = {
        "prompt": prompt,
        "domain": domain,
        "seed": seed,
        "steps": steps,
        "guidance_scale": guidance_scale,
        "width": width,
        "height": height,
    }
    if strength is not None:
        kwargs["strength"] = strength
    if negative_prompt:
        kwargs["negative_prompt"] = negative_prompt
    return kwargs


def run_text_to_image(
    db: Session,
    *,
    prompt: str,
    domain: str,
    seed: int,
    steps: int,
    guidance_scale: float,
    width: int,
    height: int,
    negative_prompt: str | None = None,
) -> dict[str, Any]:
    engine = _load_engine()
    result = engine.text_to_image(
        **_engine_kwargs(
            prompt=prompt,
            domain=domain,
            seed=seed,
            steps=steps,
            guidance_scale=guidance_scale,
            width=width,
            height=height,
            negative_prompt=negative_prompt,
        )
    )

    image_path = result.get("image_path")
    image_url_value = output_url(image_path)
    record = generation_service.create_generation(
        db,
        {
            "mode": "text_to_image",
            "domain": domain,
            "prompt": prompt,
            "negative_prompt": negative_prompt,
            "image_path": image_path,
            "image_url": image_url_value,
            "seed": seed,
            "steps": steps,
            "guidance_scale": guidance_scale,
            "width": width,
            "height": height,
            "status": "completed",
        },
    )
    return {
        "success": True,
        "image_path": image_path,
        "image_url": image_url_value,
        "metadata": record,
    }


def run_image_to_image(
    db: Session,
    *,
    uploaded_image: UploadedFile,
    prompt: str,
    domain: str,
    seed: int,
    steps: int,
    guidance_scale: float,
    strength: float,
    width: int,
    height: int,
    negative_prompt: str | None = None,
) -> dict[str, Any]:
    engine = _load_engine()
    result = engine.image_to_image(
        input_image_path=uploaded_image.file_path,
        **_engine_kwargs(
            prompt=prompt,
            domain=domain,
            seed=seed,
            steps=steps,
            guidance_scale=guidance_scale,
            strength=strength,
            width=width,
            height=height,
            negative_prompt=negative_prompt,
        ),
    )

    image_path = result.get("image_path")
    image_url_value = output_url(image_path)
    record = generation_service.create_generation(
        db,
        {
            "mode": "image_to_image",
            "domain": domain,
            "prompt": prompt,
            "negative_prompt": negative_prompt,
            "image_path": image_path,
            "image_url": image_url_value,
            "input_image_path": uploaded_image.file_path,
            "seed": seed,
            "steps": steps,
            "guidance_scale": guidance_scale,
            "strength": strength,
            "width": width,
            "height": height,
            "status": "completed",
        },
    )
    return {
        "success": True,
        "image_path": image_path,
        "image_url": image_url_value,
        "metadata": record,
    }


def run_inpaint(
    db: Session,
    *,
    uploaded_image: UploadedFile,
    uploaded_mask: UploadedFile,
    prompt: str,
    domain: str,
    seed: int,
    steps: int,
    guidance_scale: float,
    strength: float,
    width: int,
    height: int,
    negative_prompt: str | None = None,
) -> dict[str, Any]:
    engine = _load_engine()
    result = engine.inpaint(
        input_image_path=uploaded_image.file_path,
        mask_image_path=uploaded_mask.file_path,
        **_engine_kwargs(
            prompt=prompt,
            domain=domain,
            seed=seed,
            steps=steps,
            guidance_scale=guidance_scale,
            strength=strength,
            width=width,
            height=height,
            negative_prompt=negative_prompt,
        ),
    )

    image_path = result.get("image_path")
    image_url_value = output_url(image_path)
    record = generation_service.create_generation(
        db,
        {
            "mode": "inpainting",
            "domain": domain,
            "prompt": prompt,
            "negative_prompt": negative_prompt,
            "image_path": image_path,
            "image_url": image_url_value,
            "input_image_path": uploaded_image.file_path,
            "mask_image_path": uploaded_mask.file_path,
            "seed": seed,
            "steps": steps,
            "guidance_scale": guidance_scale,
            "strength": strength,
            "width": width,
            "height": height,
            "status": "completed",
        },
    )
    return {
        "success": True,
        "image_path": image_path,
        "image_url": image_url_value,
        "metadata": record,
    }
