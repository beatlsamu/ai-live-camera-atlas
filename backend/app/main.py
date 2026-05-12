from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import FRONTEND_ORIGIN, ROTATION_SECONDS
from app.core.logging import configure_logging
from app.models.channel import Channel
from app.models.observation import Observation
from app.services.channel_manager import build_channels
from app.services.memory_engine import MemoryEngine
from app.services.snapshot_fetcher import fetch_snapshot
from app.services.vision_engine import analyze_image
from app.services.llm_narrator import narrate

configure_logging()

app = FastAPI(title="AI Live Camera Atlas", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_ORIGIN, "http://localhost:5173", "http://localhost:3000", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@dataclass
class AppState:
    channels: List[Channel]
    memory: MemoryEngine
    active_index: int = 0
    last_rotation_ts: float = 0.0

    def active_channel(self) -> Channel:
        return self.channels[self.active_index]

    def has_channel(self, channel_id: str) -> bool:
        return any(c.id == channel_id for c in self.channels)

    def latest_observation(self, channel_id: str) -> Optional[Observation]:
        items = self.memory.observations_by_channel.get(channel_id, [])
        return items[-1] if items else None

    def observe(self, channel_id: str) -> Optional[Dict[str, Any]]:
        channel = next((c for c in self.channels if c.id == channel_id), None)
        if channel is None:
            return None
        image_url = fetch_snapshot(channel)
        vision = analyze_image(image_url, channel)
        recent = self.memory.get_recent(channel.id, 5)
        llm = narrate(channel, vision.dict(), recent)

        obs = Observation(
            channel_id=channel.id,
            traffic=vision.traffic,
            pedestrians=vision.pedestrians,
            weather=vision.weather,
            lighting=vision.lighting,
            anomalies=vision.anomalies or [],
            confidence=vision.confidence,
            short_narrative=llm.short_narrative,
            raw_vision=vision.dict(),
            raw_llm=llm.dict(),
        )
        self.memory.add_observation(obs)
        self.memory.set_channel_summary(channel.id, llm.channel_summary)
        self.memory.set_global_summary(llm.global_summary)
        return {"channel": channel, "observation": obs, "summary": self.memory.channel_summaries[channel.id]}

    def rotate(self) -> Channel:
        self.active_index = (self.active_index + 1) % len(self.channels)
        self.last_rotation_ts = time.time()
        return self.active_channel()

    def rotate_and_observe(self) -> Dict[str, Any]:
        channel = self.rotate()
        observation = self.observe(channel.id)
        return {"active_channel": channel, "observation": observation}

    def reseed(self) -> Dict[str, Any]:
        results = []
        for channel in self.channels:
            result = self.observe(channel.id)
            if result is not None:
                results.append(result)
        return {"ok": True, "results": results}

state = AppState(channels=build_channels(), memory=MemoryEngine())

@app.on_event("startup")
def startup_seed():
    state.observe(state.active_channel().id)

@app.get("/")
def root():
    return {
        "name": "AI Live Camera Atlas",
        "channels": len(state.channels),
        "active_channel": state.active_channel(),
    }
