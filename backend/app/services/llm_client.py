import httpx
import os
from dotenv import load_dotenv

load_dotenv(".env")

class LLMClient:
    def __init__(self):
        # Runs once when creating client
        self.base_url = os.getenv("LLM_BASE_URL")
        self.model = os.getenv("LLM_MODEL")

    async def generate(self, prompt: str) -> str:
        # Runs each LLM call
        async with httpx.AsyncClient(timeout=60) as client:
            response = await client.post(
                self.base_url + "/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False
                }
            )
            result = response.json()
            return result["response"]
        