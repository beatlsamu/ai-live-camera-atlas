from __future__ import annotations
from typing import Iterable
from app.models.observation import Observation

def summarize_observations(observations: Iterable[Observation]) -> str:
    obs = list(observations)
    if not obs:
        return "No hay observaciones suficientes todavía."
    last = obs[-1]
    return f"Resumen: último estado {last.traffic} en tráfico, {last.pedestrians} en peatones, clima {last.weather}."
