from __future__ import annotations
from dataclasses import dataclass
from typing import List
from app.models.channel import Channel
from app.models.observation import Observation

@dataclass
class LLMResult:
    short_narrative: str
    global_summary: str
    channel_summary: str
    urban_mood: str = "neutral"
    extra: dict | None = None

    def dict(self):
        return {
            "short_narrative": self.short_narrative,
            "global_summary": self.global_summary,
            "channel_summary": self.channel_summary,
            "urban_mood": self.urban_mood,
            "extra": self.extra or {},
        }

def narrate(channel: Channel, vision: dict, memory: List[Observation]) -> LLMResult:
    short = f"{channel.city} · {channel.place}: tránsito {vision['traffic']}, peatones {vision['pedestrians']}."
    channel_summary = f"{channel.city} mantiene una escena coherente con densidad {vision['traffic']} y actividad {vision['pedestrians']}."
    global_summary = f"Sistema observando múltiples canales. Último canal: {channel.city}."
    return LLMResult(short, global_summary, channel_summary, "calm", {"provider": "mock"})
