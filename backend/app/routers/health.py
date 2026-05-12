from __future__ import annotations
from fastapi import APIRouter
from datetime import datetime, timezone
from app.core.config import ROTATION_SECONDS, VISION_PROVIDER, LLM_PROVIDER

router = APIRouter(prefix="/api", tags=["health"])

@router.get("/health")
def health():
    return {
        "ok": True,
        "time": datetime.now(timezone.utc).isoformat(),
        "rotation_seconds": ROTATION_SECONDS,
        "vision_provider": VISION_PROVIDER,
        "llm_provider": LLM_PROVIDER,
    }
