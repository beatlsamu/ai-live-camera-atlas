from __future__ import annotations
from dataclasses import dataclass
from app.models.channel import Channel

@dataclass
class VisionResult:
    traffic: str = "medium"
    pedestrians: str = "medium"
    weather: str = "unknown"
    lighting: str = "unknown"
    anomalies: list[str] = None
    confidence: float = 0.72
    extra: dict | None = None

    def dict(self):
        return {
            "traffic": self.traffic,
            "pedestrians": self.pedestrians,
            "weather": self.weather,
            "lighting": self.lighting,
            "anomalies": self.anomalies or [],
            "confidence": self.confidence,
            "extra": self.extra or {},
        }

def analyze_image(image_url: str, channel: Channel) -> VisionResult:
    # Replace with your vision API or local CV model.
    return VisionResult(
        weather="unknown",
        lighting="unknown",
        anomalies=[],
        extra={"image_url": image_url, "channel": channel.id, "provider": "mock"},
    )
