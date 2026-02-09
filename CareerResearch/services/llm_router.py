import asyncio
from services.llm_clients.openai_client import call_gpt_async
from services.llm_clients.gemini_client import call_gemini_async

async def call_all_models_async(prompt: str) -> dict:
    gpt, gemini = await asyncio.gather(
        call_gpt_async(prompt),
        call_gemini_async(prompt),
        return_exceptions=True
    )

    def safe(val):
        return val if isinstance(val, str) else f"[Error] {val}"

    return {
        "GPT": safe(gpt),
        "Gemini": safe(gemini),
    }
