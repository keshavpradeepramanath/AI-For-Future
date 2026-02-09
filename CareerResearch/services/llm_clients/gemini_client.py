import requests
from config.settings import GEMINI_API_KEY

GEMINI_ENDPOINT = (
    "https://generativelanguage.googleapis.com/v1beta/"
    "models/gemini-pro:generateContent"
)

def call_gemini(prompt: str) -> str:
    try:
        response = requests.post(
            f"{GEMINI_ENDPOINT}?key={GEMINI_API_KEY}",
            json={
                "contents": [
                    {
                        "role": "user",
                        "parts": [{"text": prompt}]
                    }
                ]
            },
            timeout=30
        )

        data = response.json()

        # --- HARD FAILURES ---
        if "error" in data:
            return f"[Gemini unavailable] {data['error'].get('message', 'Unknown error')}"

        if "promptFeedback" in data:
            return "[Gemini blocked] Safety filters prevented a response."

        # --- EXPECTED PATH ---
        candidates = data.get("candidates")
        if not candidates:
            return "[Gemini unavailable] No candidates returned."

        content = candidates[0].get("content")
        if not content:
            return "[Gemini unavailable] Missing content."

        parts = content.get("parts")
        if not parts:
            return "[Gemini unavailable] Missing content parts."

        return parts[0].get("text", "[Gemini unavailable] Empty response.")

    except Exception as e:
        return f"[Gemini exception] {str(e)}"
