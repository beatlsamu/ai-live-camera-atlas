from __future__ import annotations
from pydantic import BaseModel

class Channel(BaseModel):
    id: str
    city: str
    country: str
    place: str
    type: str
    timezone: str
    provider: str
    image_url: str
    source_url: str
    refresh_seconds: int = 30
    active: bool = True
    score: float = 1.0
