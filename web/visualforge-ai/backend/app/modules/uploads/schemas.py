from datetime import datetime

from pydantic import BaseModel, ConfigDict


class UploadedFileRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    original_name: str
    file_path: str
    file_url: str
    file_type: str
    mime_type: str | None
    size_bytes: int
    created_at: datetime
