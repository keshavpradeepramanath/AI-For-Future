from services.llm_clients.openai_client import call_gpt
from services.llm_clients.gemini_client import call_gemini

def call_all_models(prompt: str) -> dict:
    return {
        "GPT": call_gpt(prompt),
        "Gemini": call_gemini(prompt),  # may return [Gemini unavailable]
    }
