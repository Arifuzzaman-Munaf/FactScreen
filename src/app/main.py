from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.app.api import router as api_router
from src.app.core.app_logging import setup_logging
from src.app.core.config import settings

setup_logging()

app = FastAPI(
    title=settings.app_name,
    version=settings.version,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/v1")


@app.get("/", tags=["meta"])
async def root():
    return {"name": settings.app_name, "version": settings.version, "health": "/v1/health"}
