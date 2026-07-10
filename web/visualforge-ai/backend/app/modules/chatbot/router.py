from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.modules.chatbot import service
from app.modules.chatbot.schemas import (
    ChatMessageCreate,
    ChatMessageRead,
    ChatMessageResponse,
)


router = APIRouter(prefix="/api/chatbot", tags=["chatbot"])


@router.post("/message", response_model=ChatMessageResponse)
def post_message(payload: ChatMessageCreate, db: Session = Depends(get_db)):
    row = service.create_message(
        db,
        message=payload.message,
        session_id=payload.session_id,
    )
    return {
        "success": True,
        "session_id": row.session_id,
        "message": row.message,
        "response": row.response,
        "created_at": row.created_at,
    }


@router.get("/history", response_model=list[ChatMessageRead])
def get_history(session_id: str = "default", db: Session = Depends(get_db)):
    return service.get_history(db, session_id=session_id)


@router.delete("/history")
def clear_history(session_id: str = "default", db: Session = Depends(get_db)):
    deleted = service.clear_history(db, session_id=session_id)
    return {"success": True, "deleted": deleted}
