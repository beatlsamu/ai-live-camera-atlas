from __future__ import annotations
from typing import Dict, List
from app.models.observation import Observation
from app.models.summary import Summary

class MemoryEngine:
    def __init__(self) -> None:
        self.observations_by_channel: Dict[str, List[Observation]] = {}
        self.channel_summaries: Dict[str, Summary] = {}
        self.global_summary: Summary = Summary(scope="global", text="Initial global summary: waiting for first observations.")

    def add_observation(self, observation: Observation) -> None:
        bucket = self.observations_by_channel.setdefault(observation.channel_id, [])
        bucket.append(observation)
        self.observations_by_channel[observation.channel_id] = bucket[-50:]

    def get_recent(self, channel_id: str, limit: int = 5) -> List[Observation]:
        return self.observations_by_channel.get(channel_id, [])[-limit:]

    def set_channel_summary(self, channel_id: str, text: str) -> None:
        self.channel_summaries[channel_id] = Summary(scope="channel", channel_id=channel_id, text=text)

    def set_global_summary(self, text: str) -> None:
        self.global_summary = Summary(scope="global", text=text)
