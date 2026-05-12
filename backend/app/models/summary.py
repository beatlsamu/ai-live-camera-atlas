from __future__ import annotations
from datetime import datetime, timezone
from typing import Optional
from pydantic import BaseModel, Field

class Summary(BaseModel):
    scope: str
    channel_id: Optional[str] = None
    text: str
    updated_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
