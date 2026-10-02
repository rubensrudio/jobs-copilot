import logging
import os

from fastapi import APIRouter, FastAPI

router = APIRouter(prefix="/api")


@router.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


def create_app() -> FastAPI:
    logging.basicConfig(
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
        level=os.getenv("LOG_LEVEL", "INFO").upper(),
    )
    app = FastAPI(title="Jobs Copilot API")
    app.include_router(router)
    return app


app = create_app()
