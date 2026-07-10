from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.ai.ai_service import get_ai_health
from app.core.config import get_settings
from app.database.session import get_db


router = APIRouter(tags=["health"])


@router.get("/health")
def health_check(db: Session = Depends(get_db)):
    settings = get_settings()
    try:
        db.execute(text("SELECT 1"))
        database_status = {"status": "ready"}
    except Exception as exc:
        database_status = {"status": "unavailable", "error": str(exc)}

    return {
        "backend": {"status": "ready"},
        "database": database_status,
        "ai": get_ai_health(),
        "available_modes": settings.available_modes,
        "available_domains": settings.available_domains,
        "storage": {
            "outputs_dir": str(settings.output_dir_path),
            "uploads_dir": str(settings.upload_dir_path),
            "outputs_url": f"{settings.API_BASE_URL.rstrip('/')}/outputs",
            "uploads_url": f"{settings.API_BASE_URL.rstrip('/')}/uploads",
        },
    }
