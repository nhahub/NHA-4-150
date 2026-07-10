from sqlalchemy import DateTime, Float, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class Generation(Base):
    __tablename__ = "generations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    mode: Mapped[str] = mapped_column(String(50), index=True, nullable=False)
    domain: Mapped[str] = mapped_column(String(80), index=True, nullable=False)
    prompt: Mapped[str] = mapped_column(Text, nullable=False)
    negative_prompt: Mapped[str | None] = mapped_column(Text, nullable=True)
    image_path: Mapped[str | None] = mapped_column(Text, nullable=True)
    image_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    input_image_path: Mapped[str | None] = mapped_column(Text, nullable=True)
    mask_image_path: Mapped[str | None] = mapped_column(Text, nullable=True)
    seed: Mapped[int | None] = mapped_column(Integer, nullable=True)
    steps: Mapped[int | None] = mapped_column(Integer, nullable=True)
    guidance_scale: Mapped[float | None] = mapped_column(Float, nullable=True)
    strength: Mapped[float | None] = mapped_column(Float, nullable=True)
    width: Mapped[int | None] = mapped_column(Integer, nullable=True)
    height: Mapped[int | None] = mapped_column(Integer, nullable=True)
    status: Mapped[str] = mapped_column(String(40), default="completed", index=True)
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[object] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
