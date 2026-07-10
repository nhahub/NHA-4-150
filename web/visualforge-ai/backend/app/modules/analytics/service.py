from sqlalchemy import Date, cast, func
from sqlalchemy.orm import Session

from app.modules.generations.models import Generation


MODE_LABELS = {
    "text_to_image": "Text-to-Image",
    "image_to_image": "Image-to-Image",
    "inpainting": "Inpainting",
}

DOMAIN_LABELS = {
    "base": "General / Base",
    "product_ads": "Product Ads",
    "egyptian_cultural": "Egyptian Cultural",
}


def get_summary(db: Session) -> dict:
    total = db.query(func.count(Generation.id)).scalar() or 0

    counts = {
        mode: db.query(func.count(Generation.id))
        .filter(Generation.mode == mode)
        .scalar()
        or 0
        for mode in MODE_LABELS
    }

    most_used = (
        db.query(Generation.domain, func.count(Generation.id).label("count"))
        .group_by(Generation.domain)
        .order_by(func.count(Generation.id).desc())
        .first()
    )

    return {
        "total_generations": total,
        "text_to_image_count": counts["text_to_image"],
        "image_to_image_count": counts["image_to_image"],
        "inpainting_count": counts["inpainting"],
        "most_used_domain": most_used.domain if most_used else None,
    }


def get_charts(db: Session) -> dict:
    over_time_rows = (
        db.query(
            cast(Generation.created_at, Date).label("date"),
            func.count(Generation.id).label("count"),
        )
        .group_by(cast(Generation.created_at, Date))
        .order_by(cast(Generation.created_at, Date).asc())
        .all()
    )

    mode_rows = (
        db.query(Generation.mode, func.count(Generation.id).label("count"))
        .group_by(Generation.mode)
        .all()
    )
    domain_rows = (
        db.query(Generation.domain, func.count(Generation.id).label("count"))
        .group_by(Generation.domain)
        .all()
    )

    mode_counts = {row.mode: row.count for row in mode_rows}
    domain_counts = {row.domain: row.count for row in domain_rows}

    return {
        "generations_over_time": [
            {"date": row.date.isoformat(), "count": row.count} for row in over_time_rows
        ],
        "mode_distribution": [
            {
                "mode": mode,
                "label": MODE_LABELS[mode],
                "count": mode_counts.get(mode, 0),
            }
            for mode in MODE_LABELS
        ],
        "domain_usage": [
            {
                "domain": domain,
                "label": DOMAIN_LABELS[domain],
                "count": domain_counts.get(domain, 0),
            }
            for domain in DOMAIN_LABELS
        ],
    }
