
from __future__ import annotations
import os
from datetime import datetime, timezone
from typing import Any, Dict, List, Literal
from uuid import uuid4

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from services.vision.nvidia_vision import NvidiaVisionProvider
from services.llm.nvidia_llm import NvidiaLLMProvider

load_dotenv()

FRONTEND_ORIGIN = os.getenv("FRONTEND_ORIGIN", "*")
ROTATION_SECONDS = int(os.getenv("ROTATION_SECONDS", "30"))

app = FastAPI(title="AI Live Camera Atlas", version="0.2.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_ORIGIN, "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

ChannelType = Literal["traffic", "airport", "city"]

class Channel(BaseModel):
    id: str
    city: str
    country: str
    place: str
    type: ChannelType
    timezone: str
    provider: str
    image_url: str
    source_url: str

class Observation(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    channel_id: str
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    narrative: str = ""
    vision_data: Dict[str, Any] = Field(default_factory=dict)

CHANNELS = [
    Channel(
        id="tokyo-shibuya",
        city="Tokyo",
        country="Japan",
        place="Shibuya Crossing",
        type="city",
        timezone="Asia/Tokyo",
        provider="windy",
        image_url="https://images.unsplash.com/photo-1540959733332-eab4deabeeaf?q=80&w=1200&auto=format&fit=crop",
        source_url="https://www.windy.com/",
    ),
    Channel(
        id="santiago-alameda",
        city="Santiago",
        country="Chile",
        place="Alameda Centro",
        type="traffic",
        timezone="America/Santiago",
        provider="traffic",
        image_url="https://images.unsplash.com/photo-1519302959554-a75be0afc82a?q=80&w=1200&auto=format&fit=crop",
        source_url="https://www.transporteinforma.cl/",
    ),
]

ACTIVE_INDEX = 0
OBSERVATIONS_BY_CHANNEL = {c.id: [] for c in CHANNELS}

VISION = NvidiaVisionProvider()
LLM = NvidiaLLMProvider()

def get_active_channel():
    return CHANNELS[ACTIVE_INDEX]

def rotate_channel():
    global ACTIVE_INDEX
    ACTIVE_INDEX = (ACTIVE_INDEX + 1) % len(CHANNELS)
    return get_active_channel()

def ingest_observation(channel: Channel):
    vision_result = VISION.analyze(channel.image_url, channel)
    memory = OBSERVATIONS_BY_CHANNEL[channel.id][-5:]
    llm_result = LLM.narrate(channel, vision_result, memory)

    obs = Observation(
        channel_id=channel.id,
        narrative=llm_result.get("narrative", ""),
        vision_data=vision_result,
    )

    OBSERVATIONS_BY_CHANNEL[channel.id].append(obs)
    return obs

@app.on_event("startup")
def startup_seed():
    ingest_observation(get_active_channel())

@app.get("/api/health")
def health():
    return {"ok": True}

@app.get("/api/channels")
def channels():
    return {"items": CHANNELS}

@app.get("/api/channels/active")
def active_channel():
    channel = get_active_channel()
    latest = OBSERVATIONS_BY_CHANNEL[channel.id][-1]
    return {"channel": channel, "latest_observation": latest}

@app.post("/api/rotate")
def rotate():
    channel = rotate_channel()
    obs = ingest_observation(channel)
    return {"channel": channel, "observation": obs}
