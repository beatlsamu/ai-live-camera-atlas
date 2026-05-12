from __future__ import annotations
from fastapi import APIRouter, HTTPException
from app.main import state

router = APIRouter(prefix="/api", tags=["analysis"])

@router.post("/rotate")
def rotate():
    return state.rotate_and_observe()

@router.post("/reseed")
def reseed():
    return state.reseed()

@router.get("/summary/global")
def global_summary():
    return {
        "summary": state.memory.global_summary,
        "active_channel": state.active_channel(),
        "recent_by_channel": {
            channel_id: observations[-3:]
            for channel_id, observations in state.memory.observations_by_channel.items()
        },
    }
