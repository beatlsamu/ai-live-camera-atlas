import os
import requests

API_KEY = os.getenv("NVIDIA_API_KEY")

VISION_MODEL = os.getenv(
    "NVIDIA_VISION_MODEL",
    "google/paligemma"
)

VISION_URL = f"https://ai.api.nvidia.com/v1/vlm/{VISION_MODEL}"


class NvidiaVisionProvider:

    def analyze(self, image_url, channel):

        prompt = f"""
        Analyze this live urban camera scene from:

        City: {channel.city}
        Place: {channel.place}
        Country: {channel.country}

        Return a detailed analysis including:

        - traffic density
        - pedestrian density
        - weather conditions
        - lighting conditions
        - visibility quality
        - possible incidents
        - unusual behavior
        - congestion level
        - environmental atmosphere
        - time-of-day interpretation

        Keep the response structured and concise.
        """

        payload = {
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt
                        },
                        {
                            "type": "image_url",
                            "image_url": image_url
                        }
                    ]
                }
            ],
            "temperature": 0.2,
            "top_p": 0.7,
            "max_tokens": 512,
            "stream": False
        }

        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "accept": "application/json",
            "content-type": "application/json"
        }

        try:

            response = requests.post(
                VISION_URL,
                json=payload,
                headers=headers,
                timeout=60
            )

            return response.json()

        except Exception as e:

            return {
                "error": str(e)
            }
