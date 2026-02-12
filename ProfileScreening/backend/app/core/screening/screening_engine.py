import json
from app.core.llm.openai_client import call_gpt_async


SELECTION_THRESHOLD = 70
MAX_MUST_HAVE_MISSES = 1


async def screen_candidate(job_description: str, candidate_profile: str):
    prompt = f"""
You are a hiring evaluation engine.

JOB DESCRIPTION:
{job_description}

CANDIDATE PROFILE:
{candidate_profile}

Return STRICT JSON ONLY in this format:

{{
  "score": <number between 0 and 100>,
  "must_have_missing_count": <integer>,
  "strong_matches": ["..."],
  "critical_gaps": ["..."],
  "reasoning": "..."
}}

Scoring Rules:
- 90+ = Exceptional
- 75-89 = Strong
- 60-74 = Moderate
- Below 60 = Weak

Be realistic and conservative in scoring.
"""

    response = await call_gpt_async(prompt, temperature=0.1)

    # Extract JSON safely
    try:
        data = json.loads(response)
    except Exception:
        # fallback in case model adds extra text
        start = response.find("{")
        end = response.rfind("}") + 1
        data = json.loads(response[start:end])

    score = data["score"]
    missing = data["must_have_missing_count"]

    # Deterministic decision logic
    if missing > MAX_MUST_HAVE_MISSES:
        decision = "REJECT"
        score = min(score, 65)  # Force lower score to reflect rejection

    elif score < SELECTION_THRESHOLD:
        decision = "REJECT"

    else:
        decision = "SELECT"

    return {
        "score": score,
        "decision": decision,
        "strong_matches": data["strong_matches"],
        "critical_gaps": data["critical_gaps"],
        "reasoning": data["reasoning"]
    }
