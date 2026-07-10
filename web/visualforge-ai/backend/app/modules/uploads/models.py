from sqlalchemy import BigInteger, DateTime, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class UploadedFile(Base):
    __tablename__ = "uploaded_files"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    original_name: Mapped[str] = mapped_column(String(255), nullable=False)
    file_path: Mapped[str] = mapped_column(Text, nullable=False)
    file_url: Mapped[str] = mapped_column(Text, nullable=False)
    file_type: Mapped[str] = mapped_column(String(80), nullable=False)
    mime_type: Mapped[str | None] = mapped_column(String(120), nullable=True)
    size_bytes: Mapped[int] = mapped_column(BigInteger, nullable=False)
    created_at: Mapped[object] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
