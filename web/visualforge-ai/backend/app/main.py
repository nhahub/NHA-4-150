from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.core.config import get_settings
from app.core.cors import setup_cors
from app.modules.analytics.router import router as analytics_router
from app.modules.chatbot.router import router as chatbot_router
from app.modules.generations.router import router as generations_router
from app.modules.health.router import router as health_router
from app.modules.uploads.router import router as uploads_router


def create_app() -> FastAPI:
    settings = get_settings()
    settings.ensure_storage()

    app = FastAPI(
        title="VisualForge AI API",
        version="1.0.0",
        description="Inference API and history backend for VisualForge AI.",
    )
    setup_cors(app)

    app.mount(
        "/outputs",
        StaticFiles(directory=str(settings.output_dir_path)),
        name="outputs",
    )
    app.mount(
        "/uploads",
        StaticFiles(directory=str(settings.upload_dir_path)),
        name="uploads",
    )

    app.include_router(health_router)
    app.include_router(generations_router)
    app.include_router(uploads_router)
    app.include_router(analytics_router)
    app.include_router(chatbot_router)

    @app.get("/")
    def root():
        return {
            "message": "VisualForge AI backend is running",
            "docs": "/docs",
            "health": "/health",
        }

    return app


app = create_app()
