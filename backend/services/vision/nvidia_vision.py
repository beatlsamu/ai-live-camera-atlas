
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

        prompt = '''
        Analyze this urban live camera scene.
        Return:
        - traffic density
        - pedestrian density
        - weather
        - lighting
        - unusual activity
        '''

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
    "type": "image",
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

        response = requests.post(
            VISION_URL,
            json=payload,
            headers=headers,
            timeout=60
        )

        try:
            return response.json()
        except Exception:
            return {"error": response.text}
