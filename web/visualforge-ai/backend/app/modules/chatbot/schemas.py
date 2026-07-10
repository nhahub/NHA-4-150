from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ChatMessageCreate(BaseModel):
    message: str
    session_id: str = "default"


class ChatMessageRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    session_id: str
    sender: str
    message: str
    response: str
    created_at: datetime


class ChatMessageResponse(BaseModel):
    success: bool
    session_id: str
    message: str
    response: str
    created_at: datetime
