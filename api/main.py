from fastapi import FastAPI
import uvicorn

from api.core.config import settings
from api.core.logging import get_logger, setup_logging
from api.src.users.routes import router as auth_router
from api.utils.migrations import run_migrations

setup_logging()

run_migrations()

logger = get_logger(__name__)

app = FastAPI(
    title=settings.PROJECT_NAME,
    debug=settings.DEBUG,
)

app.include_router(auth_router)


@app.get("/health")
async def health_check():
    return {"status": "ok"}


@app.get("/")
async def root():
    logger.debug("Root endpoint called")
    return {"message": "Welcome to Hero API!"}


if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=settings.UVICORN_PORT,
    )
