from datetime import datetime

from pydantic import BaseModel, ConfigDict


class GenerationBase(BaseModel):
    mode: str
    domain: str
    prompt: str
    negative_prompt: str | None = None
    image_path: str | None = None
    image_url: str | None = None
    input_image_path: str | None = None
    mask_image_path: str | None = None
    seed: int | None = None
    steps: int | None = None
    guidance_scale: float | None = None
    strength: float | None = None
    width: int | None = None
    height: int | None = None
    status: str = "completed"
    error_message: str | None = None


class GenerationCreate(GenerationBase):
    pass


class GenerationRead(GenerationBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime


class GenerationRunResponse(BaseModel):
    success: bool
    image_path: str | None
    image_url: str | None
    metadata: GenerationRead
