from __future__ import annotations
from app.models.channel import Channel

def fetch_snapshot(channel: Channel) -> str:
    # Future: fetch remote image bytes, cache, validate.
    return channel.image_url
