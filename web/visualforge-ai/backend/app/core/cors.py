from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import get_settings


def setup_cors(app: FastAPI) -> None:
    settings = get_settings()
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            settings.FRONTEND_ORIGIN,
            "http://127.0.0.1:5173",
            "http://localhost:5173",
        ],
        allow_origin_regex=r"http://localhost:\d+|http://127\.0\.0\.1:\d+",
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
