import requests
import asyncio
from functools import partial
from config.settings import GEMINI_API_KEY

GEMINI_ENDPOINT = (
    "https://generativelanguage.googleapis.com/v1beta/"
    "models/gemini-pro:generateContent"
)

def _call_gemini_sync(prompt: str) -> str:
    response = requests.post(
        f"{GEMINI_ENDPOINT}?key={GEMINI_API_KEY}",
        json={
            "contents": [
                {"role": "user", "parts": [{"text": prompt}]}
            ]
        },
        timeout=30
    )
    data = response.json()

    if "candidates" not in data:
        return "[Gemini unavailable]"

    return data["candidates"][0]["content"]["parts"][0]["text"]

async def call_gemini_async(prompt: str) -> str:
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(
        None, partial(_call_gemini_sync, prompt)
    )
