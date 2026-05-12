from __future__ import annotations
from fastapi import APIRouter
from app.main import state

router = APIRouter(prefix="/api", tags=["memory"])

@router.get("/memory")
def memory():
    return {
        "active_channel_id": state.active_channel().id,
        "channel_summaries": state.memory.channel_summaries,
        "global_summary": state.memory.global_summary,
        "recent_counts": {
            channel_id: len(items)
            for channel_id, items in state.memory.observations_by_channel.items()
        },
    }
