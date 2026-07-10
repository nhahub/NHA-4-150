from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.ai import ai_service
from app.database.session import get_db
from app.modules.generations import service
from app.modules.generations.schemas import GenerationRead, GenerationRunResponse
from app.modules.uploads import service as upload_service


router = APIRouter(prefix="/api", tags=["generations"])


@router.post("/text-to-image", response_model=GenerationRunResponse)
def text_to_image(
    prompt: str = Form(...),
    domain: str = Form("base"),
    seed: int = Form(42),
    steps: int = Form(30),
    guidance_scale: float = Form(7.5),
    width: int = Form(1024),
    height: int = Form(1024),
    negative_prompt: str | None = Form(None),
    db: Session = Depends(get_db),
):
    try:
        return ai_service.run_text_to_image(
            db,
            prompt=prompt,
            domain=domain,
            seed=seed,
            steps=steps,
            guidance_scale=guidance_scale,
            width=width,
            height=height,
            negative_prompt=negative_prompt,
        )
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.post("/image-to-image", response_model=GenerationRunResponse)
def image_to_image(
    image: UploadFile = File(...),
    prompt: str = Form(...),
    domain: str = Form("base"),
    seed: int = Form(123),
    steps: int = Form(30),
    guidance_scale: float = Form(7.5),
    strength: float = Form(0.35),
    width: int = Form(1024),
    height: int = Form(1024),
    negative_prompt: str | None = Form(None),
    db: Session = Depends(get_db),
):
    try:
        uploaded_image = upload_service.save_upload_file(db, image, "input_image")
        return ai_service.run_image_to_image(
            db,
            uploaded_image=uploaded_image,
            prompt=prompt,
            domain=domain,
            seed=seed,
            steps=steps,
            guidance_scale=guidance_scale,
            strength=strength,
            width=width,
            height=height,
            negative_prompt=negative_prompt,
        )
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.post("/inpaint", response_model=GenerationRunResponse)
def inpaint(
    image: UploadFile = File(...),
    mask: UploadFile = File(...),
    prompt: str = Form(...),
    domain: str = Form("base"),
    seed: int = Form(777),
    steps: int = Form(30),
    guidance_scale: float = Form(7.5),
    strength: float = Form(0.45),
    width: int = Form(1024),
    height: int = Form(1024),
    negative_prompt: str | None = Form(None),
    db: Session = Depends(get_db),
):
    try:
        uploaded_image = upload_service.save_upload_file(db, image, "input_image")
        uploaded_mask = upload_service.save_upload_file(db, mask, "mask_image")
        return ai_service.run_inpaint(
            db,
            uploaded_image=uploaded_image,
            uploaded_mask=uploaded_mask,
            prompt=prompt,
            domain=domain,
            seed=seed,
            steps=steps,
            guidance_scale=guidance_scale,
            strength=strength,
            width=width,
            height=height,
            negative_prompt=negative_prompt,
        )
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.get("/generations", response_model=list[GenerationRead])
def list_generations(
    search: str | None = None,
    mode: str | None = None,
    domain: str | None = None,
    sort: str = "newest",
    db: Session = Depends(get_db),
):
    return service.list_generations(
        db,
        search=search,
        mode=mode,
        domain=domain,
        sort=sort,
    )


@router.get("/generations/{generation_id}", response_model=GenerationRead)
def get_generation(generation_id: int, db: Session = Depends(get_db)):
    generation = service.get_generation(db, generation_id)
    if not generation:
        raise HTTPException(status_code=404, detail="Generation not found")
    return generation


@router.delete("/generations/{generation_id}")
def delete_generation(generation_id: int, db: Session = Depends(get_db)):
    generation = service.get_generation(db, generation_id)
    if not generation:
        raise HTTPException(status_code=404, detail="Generation not found")
    service.delete_generation(db, generation)
    return {"success": True, "deleted_id": generation_id}
