import logging
import os
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import APIRouter, FastAPI

from app.config import Settings, get_settings
from app.db import ensure_indexes, get_db
from app.errors import register_error_handlers

router = APIRouter(prefix="/api")


@router.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    ensure_indexes(get_db())
    yield


def create_app(settings: Settings | None = None) -> FastAPI:
    logging.basicConfig(
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
        level=os.getenv("LOG_LEVEL", "INFO").upper(),
    )
    app = FastAPI(title="Jobs Copilot API", lifespan=lifespan)
    app.include_router(router)

    if settings is not None:
        app.dependency_overrides[get_settings] = lambda: settings
    register_error_handlers(app)

    return app


app = create_app()
