from sqlalchemy import DateTime, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    session_id: Mapped[str] = mapped_column(String(120), index=True, nullable=False)
    sender: Mapped[str] = mapped_column(String(40), nullable=False, default="user")
    message: Mapped[str] = mapped_column(Text, nullable=False)
    response: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[object] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
