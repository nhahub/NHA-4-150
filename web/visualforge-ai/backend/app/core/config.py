import os
from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


BACKEND_DIR = Path(__file__).resolve().parents[2]
PROJECT_DIR = BACKEND_DIR.parent
APP_DIR = BACKEND_DIR / "app"


def _resolve_path(raw_path: str | None, fallback: Path) -> Path:
    if not raw_path:
        return fallback

    path = Path(raw_path)
    if path.is_absolute():
        return path

    normalized = raw_path.replace("\\", "/")
    if normalized.startswith("backend/"):
        return (PROJECT_DIR / path).resolve()
    if normalized.startswith("app/"):
        return (BACKEND_DIR / path).resolve()
    return (BACKEND_DIR / path).resolve()


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=str(BACKEND_DIR / ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=True,
    )

    APP_NAME: str = "VisualForge AI"
    API_BASE_URL: str = "http://localhost:8000"
    FRONTEND_ORIGIN: str = "http://localhost:5173"
    DATABASE_URL: str = (
        "postgresql+psycopg2://visualforge_user:visualforge_password"
        "@localhost:5432/visualforge_db"
    )
    VISUALFORGE_OUTPUT_DIR: str = str(APP_DIR / "storage" / "outputs")
    VISUALFORGE_UPLOAD_DIR: str = str(APP_DIR / "storage" / "uploads")
    EGYPTIAN_LORA_DIR: str = "path/to/egyptian/lora"
    PRODUCT_LORA_DIR: str = "path/to/product/lora"

    @property
    def output_dir_path(self) -> Path:
        return _resolve_path(
            self.VISUALFORGE_OUTPUT_DIR,
            APP_DIR / "storage" / "outputs",
        )

    @property
    def upload_dir_path(self) -> Path:
        return _resolve_path(
            self.VISUALFORGE_UPLOAD_DIR,
            APP_DIR / "storage" / "uploads",
        )

    @property
    def available_modes(self) -> list[dict[str, str]]:
        return [
            {"value": "text_to_image", "label": "Text-to-Image"},
            {"value": "image_to_image", "label": "Image-to-Image"},
            {"value": "inpainting", "label": "Inpainting"},
        ]

    @property
    def available_domains(self) -> list[dict[str, str]]:
        return [
            {"value": "base", "label": "General / Base"},
            {"value": "product_ads", "label": "Product Ads"},
            {"value": "egyptian_cultural", "label": "Egyptian Cultural"},
        ]

    def ensure_storage(self) -> None:
        self.output_dir_path.mkdir(parents=True, exist_ok=True)
        self.upload_dir_path.mkdir(parents=True, exist_ok=True)

    def sync_ai_environment(self) -> None:
        self.ensure_storage()
        os.environ["VISUALFORGE_OUTPUT_DIR"] = str(self.output_dir_path)
        os.environ["VISUALFORGE_UPLOAD_DIR"] = str(self.upload_dir_path)
        os.environ["EGYPTIAN_LORA_DIR"] = self.EGYPTIAN_LORA_DIR
        os.environ["PRODUCT_LORA_DIR"] = self.PRODUCT_LORA_DIR


@lru_cache
def get_settings() -> Settings:
    settings = Settings()
    settings.ensure_storage()
    return settings
