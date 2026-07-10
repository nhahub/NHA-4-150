from sqlalchemy.orm import Session

from app.modules.chatbot.models import ChatMessage


def build_response(message: str) -> str:
    text = message.lower().strip()
    if any(word in text for word in ["domain", "egyptian", "product"]):
        return (
            "Use domains to steer style: General / Base for flexible images, "
            "Product Ads for commercial compositions, and Egyptian Cultural for heritage-inspired visuals."
        )
    if any(word in text for word in ["inpaint", "mask", "edit"]):
        return (
            "For inpainting, upload the source image and a mask. The white mask area is the region "
            "the studio edits using your prompt."
        )
    if any(word in text for word in ["image-to-image", "img2img", "strength"]):
        return (
            "Image-to-Image uses your uploaded image as structure. Lower strength preserves more of "
            "the original, while higher strength gives the model more freedom."
        )
    if any(word in text for word in ["seed", "steps", "guidance"]):
        return (
            "Seed controls repeatability, steps control refinement time, and guidance scale controls "
            "how strongly the prompt shapes the result."
        )
    return (
        "I can help with VisualForge studio modes, prompt settings, domains, uploads, masks, "
        "and gallery history."
    )


def create_message(db: Session, *, message: str, session_id: str = "default") -> ChatMessage:
    response = build_response(message)
    row = ChatMessage(
        session_id=session_id,
        sender="user",
        message=message,
        response=response,
    )
    db.add(row)
    db.commit()
    db.refresh(row)
    return row


def get_history(db: Session, session_id: str = "default") -> list[ChatMessage]:
    return (
        db.query(ChatMessage)
        .filter(ChatMessage.session_id == session_id)
        .order_by(ChatMessage.created_at.asc())
        .all()
    )


def clear_history(db: Session, session_id: str = "default") -> int:
    rows = db.query(ChatMessage).filter(ChatMessage.session_id == session_id).all()
    deleted = len(rows)
    for row in rows:
        db.delete(row)
    db.commit()
    return deleted
