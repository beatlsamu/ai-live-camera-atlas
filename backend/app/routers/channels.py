from __future__ import annotations
from fastapi import APIRouter, HTTPException
from app.main import state
from app.services.channel_manager import build_channels

router = APIRouter(prefix="/api", tags=["channels"])

@router.get("/channels")
def list_channels():
    return {"items": state.channels, "count": len(state.channels)}

@router.get("/channels/active")
def active_channel():
    channel = state.active_channel()
    latest = state.latest_observation(channel.id)
    return {"channel": channel, "latest_observation": latest}

@router.post("/channels/{channel_id}/observe")
def observe_channel(channel_id: str):
    result = state.observe(channel_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Channel not found")
    return result

@router.get("/channels/{channel_id}/summary")
def channel_summary(channel_id: str):
    if not state.has_channel(channel_id):
        raise HTTPException(status_code=404, detail="Channel not found")
    return {
        "summary": state.memory.channel_summaries.get(
            channel_id,
            {"scope": "channel", "channel_id": channel_id, "text": "No summary yet."},
        ),
        "observations": state.memory.observations_by_channel.get(channel_id, [])[-10:],
    }
