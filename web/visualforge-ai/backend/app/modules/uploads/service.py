import uuid
from pathlib import Path

from fastapi import UploadFile
from sqlalchemy.orm import Session

from app.ai.ai_service import upload_url
from app.core.config import get_settings
from app.modules.uploads.models import UploadedFile as UploadedFileModel


def _safe_suffix(filename: str | None) -> str:
    suffix = Path(filename or "").suffix.lower()
    return suffix if suffix else ".png"


def save_upload_file(
    db: Session,
    file: UploadFile,
    file_type: str = "input_image",
) -> UploadedFileModel:
    settings = get_settings()
    settings.ensure_storage()

    contents = file.file.read()
    filename = f"{uuid.uuid4().hex}{_safe_suffix(file.filename)}"
    file_path = settings.upload_dir_path / filename
    file_path.write_bytes(contents)

    stored = UploadedFileModel(
        original_name=file.filename or filename,
        file_path=str(file_path),
        file_url=upload_url(str(file_path)) or "",
        file_type=file_type,
        mime_type=file.content_type,
        size_bytes=len(contents),
    )
    db.add(stored)
    db.commit()
    db.refresh(stored)
    return stored
