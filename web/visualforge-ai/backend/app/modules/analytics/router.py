from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.modules.analytics import service


router = APIRouter(prefix="/api/analytics", tags=["analytics"])


@router.get("/summary")
def analytics_summary(db: Session = Depends(get_db)):
    return service.get_summary(db)


@router.get("/charts")
def analytics_charts(db: Session = Depends(get_db)):
    return service.get_charts(db)
