
import os
import requests

API_KEY = os.getenv("NVIDIA_API_KEY")

LLM_MODEL = os.getenv(
    "NVIDIA_LLM_MODEL",
    "meta/llama-3.1-8b-instruct"
)

LLM_URL = "https://integrate.api.nvidia.com/v1/chat/completions"

class NvidiaLLMProvider:

    def narrate(self, channel, vision_result, memory):

        prompt = f'''
        You are a global urban observer AI.

        City: {channel.city}
        Place: {channel.place}

        Vision analysis:
        {vision_result}

        Previous memory:
        {memory}

        Generate:
        - narration
        - urban interpretation
        - temporal analysis
        '''

        payload = {
            "model": LLM_MODEL,
            "messages": [
                {
                    "role": "system",
                    "content": "You are an AI narrator for global urban observations."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": 0.4,
            "top_p": 0.7,
            "max_tokens": 512,
            "stream": False
        }

        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }

        response = requests.post(
            LLM_URL,
            json=payload,
            headers=headers,
            timeout=60
        )

        try:
            data = response.json()
            text = data["choices"][0]["message"]["content"]

            return {
                "narrative": text,
                "raw": data
            }

        except Exception:
            return {
                "narrative": "Unable to generate narration.",
                "raw": response.text
            }
