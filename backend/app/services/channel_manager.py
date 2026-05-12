from __future__ import annotations
from typing import List
from app.models.channel import Channel
from app.integrations.dgac import DGAC_CHANNELS
from app.integrations.windy import WINDY_CHANNELS
from app.integrations.traffic import TRAFFIC_CHANNELS
from app.integrations.generic_webcam import GENERIC_CHANNELS

def build_channels() -> List[Channel]:
    raw = DGAC_CHANNELS + WINDY_CHANNELS + TRAFFIC_CHANNELS + GENERIC_CHANNELS
    seen = set()
    channels: List[Channel] = []
    for item in raw:
        if item["id"] in seen:
            continue
        seen.add(item["id"])
        channels.append(Channel(**item))
    return channels
