from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


# Imported for Alembic autogeneration metadata discovery.
from app.modules.chatbot import models as chatbot_models  # noqa: E402,F401
from app.modules.generations import models as generation_models  # noqa: E402,F401
from app.modules.uploads import models as upload_models  # noqa: E402,F401
