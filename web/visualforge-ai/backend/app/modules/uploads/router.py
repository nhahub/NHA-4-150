from fastapi import APIRouter, Depends, File, Form, UploadFile
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.modules.uploads import service
from app.modules.uploads.schemas import UploadedFileRead


router = APIRouter(prefix="/api", tags=["uploads"])


@router.post("/uploads", response_model=UploadedFileRead)
def upload_file(
    file: UploadFile = File(...),
    file_type: str = Form("asset"),
    db: Session = Depends(get_db),
):
    return service.save_upload_file(db, file, file_type)
