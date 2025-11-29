from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.app.api import router as api_router
from src.app.core.app_logging import setup_logging
from src.app.core.config import settings

setup_logging()

# Initialize FastAPI app
app = FastAPI(
    title=settings.app_name,
    version=settings.version,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API router
app.include_router(api_router, prefix="/v1")

# Root endpoint
@app.get("/", tags=["meta"])
async def root():
    # Return app name, version, and health check endpoint
    return {"name": settings.app_name, "version": settings.version, "health": "/v1/health"}