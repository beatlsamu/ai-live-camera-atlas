from __future__ import annotations
from datetime import datetime, timezone
from typing import Any, Dict, List
from uuid import uuid4
from pydantic import BaseModel, Field

class Observation(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    channel_id: str
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    traffic: str = "unknown"
    pedestrians: str = "unknown"
    weather: str = "unknown"
    lighting: str = "unknown"
    anomalies: List[str] = Field(default_factory=list)
    confidence: float = 0.0
    short_narrative: str = ""
    raw_vision: Dict[str, Any] = Field(default_factory=dict)
    raw_llm: Dict[str, Any] = Field(default_factory=dict)
