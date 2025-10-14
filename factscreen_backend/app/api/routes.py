from fastapi import APIRouter

router = APIRouter()

@router.get("/ping", tags=["health"])  # liveness probe under /v1
def ping() -> dict:
    return {"message": "pong"}

