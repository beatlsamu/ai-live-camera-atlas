from __future__ import annotations
import os

FRONTEND_ORIGIN = os.getenv("FRONTEND_ORIGIN", "http://localhost:5173")
ROTATION_SECONDS = int(os.getenv("ROTATION_SECONDS", "30"))
VISION_PROVIDER = os.getenv("VISION_PROVIDER", "mock")
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "mock")
VISION_API_URL = os.getenv("VISION_API_URL", "")
LLM_API_URL = os.getenv("LLM_API_URL", "")
VISION_API_KEY = os.getenv("VISION_API_KEY", "")
LLM_API_KEY = os.getenv("LLM_API_KEY", "")
