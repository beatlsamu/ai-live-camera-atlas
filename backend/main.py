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

# =========================
# ENVIRONMENT
# =========================

load_dotenv()

FRONTEND_ORIGIN = os.getenv("FRONTEND_ORIGIN", "*")
ROTATION_SECONDS = int(os.getenv("ROTATION_SECONDS", "30"))

# =========================
# FASTAPI
# =========================

app = FastAPI(
    title="AI Live Camera Atlas",
    version="0.3.0"
)

# =========================
# CORS
# =========================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        FRONTEND_ORIGIN,
        "http://localhost:5173",
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# TYPES
# =========================

ChannelType = Literal[
    "traffic",
    "airport",
    "city"
]

# =========================
# MODELS
# =========================

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

    timestamp: str = Field(
        default_factory=lambda: datetime.now(
            timezone.utc
        ).isoformat()
    )

    narrative: str = ""

    vision_data: Dict[str, Any] = Field(
        default_factory=dict
    )


# =========================
# CHANNELS
# =========================

CHANNELS: List[Channel] = [

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

    Channel(
        id="newyork-times-square",
        city="New York",
        country="USA",
        place="Times Square",
        type="city",
        timezone="America/New_York",
        provider="earthcam",
        image_url="https://images.unsplash.com/photo-1534430480872-3498386e7856?q=80&w=1200&auto=format&fit=crop",
        source_url="https://www.earthcam.com/",
    ),
]

# =========================
# STATE
# =========================

ACTIVE_INDEX = 0

OBSERVATIONS_BY_CHANNEL: Dict[
    str,
    List[Observation]
] = {
    c.id: [] for c in CHANNELS
}

# =========================
# PROVIDERS
# =========================

VISION = NvidiaVisionProvider()
LLM = NvidiaLLMProvider()

# =========================
# HELPERS
# =========================

def get_active_channel() -> Channel:
    return CHANNELS[ACTIVE_INDEX]


def rotate_channel() -> Channel:
    global ACTIVE_INDEX

    ACTIVE_INDEX = (
        ACTIVE_INDEX + 1
    ) % len(CHANNELS)

    return get_active_channel()


def ingest_observation(
    channel: Channel
) -> Observation:

    # =====================
    # VISION ANALYSIS
    # =====================

    vision_result = VISION.analyze(
        channel.image_url,
        channel
    )

    # =====================
    # TEMPORAL MEMORY
    # =====================

    memory = OBSERVATIONS_BY_CHANNEL[
        channel.id
    ][-5:]

    # =====================
    # LLM NARRATION
    # =====================

    llm_result = LLM.narrate(
        channel,
        vision_result,
        memory
    )

    narrative = ""

    if isinstance(llm_result, dict):
        narrative = llm_result.get(
            "narrative",
            ""
        )

    # =====================
    # OBSERVATION OBJECT
    # =====================

    obs = Observation(
        channel_id=channel.id,
        narrative=narrative,
        vision_data=vision_result,
    )

    OBSERVATIONS_BY_CHANNEL[
        channel.id
    ].append(obs)

    return obs


def build_global_summary():

    summaries = []

    for channel_id, observations in OBSERVATIONS_BY_CHANNEL.items():

        if observations:

            latest = observations[-1]

            if latest.narrative:
                summaries.append(latest.narrative)

    return {
        "active_channels": len(CHANNELS),
        "observations": len(summaries),
        "summary": " ".join(summaries[:3])
    }

# =========================
# STARTUP
# =========================

@app.on_event("startup")
def startup_seed():

    try:
        ingest_observation(
            get_active_channel()
        )

    except Exception as e:
        print("Startup ingestion error:", e)

# =========================
# HEALTH
# =========================

@app.get("/")
def root():
    return {
        "name": "AI Live Camera Atlas",
        "status": "online",
        "version": "0.3.0"
    }


@app.get("/api/health")
def health():
    return {
        "status": "ok",
        "service": "ai-live-camera-atlas",
        "version": "0.3.0",
        "channels": len(CHANNELS),
    }

# =========================
# CHANNELS
# =========================

@app.get("/api/channels")
def channels():
    return {
        "items": CHANNELS
    }


@app.get("/api/channels/active")
def active_channel():

    channel = get_active_channel()

    observations = OBSERVATIONS_BY_CHANNEL[
        channel.id
    ]

    latest = (
        observations[-1]
        if observations
        else None
    )

    return {
        "channel": channel,
        "latest_observation": latest,
        "rotation_seconds": ROTATION_SECONDS,
    }

# =========================
# ROTATION
# =========================

@app.post("/api/rotate")
def rotate():

    channel = rotate_channel()

    obs = ingest_observation(channel)

    return {
        "channel": channel,
        "observation": obs,
    }

# =========================
# MEMORY
# =========================

@app.get("/api/memory/{channel_id}")
def memory(channel_id: str):

    return {
        "channel_id": channel_id,
        "observations": OBSERVATIONS_BY_CHANNEL.get(
            channel_id,
            []
        )
    }

# =========================
# WORLD SUMMARY
# =========================

@app.get("/api/world/summary")
def world_summary():

    return build_global_summary()
