from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.modules.generations.models import Generation


def create_generation(db: Session, data: dict) -> Generation:
    generation = Generation(**data)
    db.add(generation)
    db.commit()
    db.refresh(generation)
    return generation


def list_generations(
    db: Session,
    *,
    search: str | None = None,
    mode: str | None = None,
    domain: str | None = None,
    sort: str = "newest",
) -> list[Generation]:
    query = db.query(Generation)

    if search:
        pattern = f"%{search}%"
        query = query.filter(
            or_(
                Generation.prompt.ilike(pattern),
                Generation.domain.ilike(pattern),
                Generation.mode.ilike(pattern),
            )
        )
    if mode and mode != "all":
        query = query.filter(Generation.mode == mode)
    if domain and domain != "all":
        query = query.filter(Generation.domain == domain)

    if sort == "oldest":
        query = query.order_by(Generation.created_at.asc())
    else:
        query = query.order_by(Generation.created_at.desc())

    return query.all()


def get_generation(db: Session, generation_id: int) -> Generation | None:
    return db.get(Generation, generation_id)


def delete_generation(db: Session, generation: Generation) -> None:
    db.delete(generation)
    db.commit()
