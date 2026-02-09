from services.llm_clients.openai_client import call_gpt_async

async def generate_resume_improvements(gap_analysis: str) -> str:
    prompt = f"""
You are a senior career coach.

Based on this resume gap analysis:
{gap_analysis}

Provide ACTIONABLE guidance:

## What to Add
## What to Rewrite
## What to Remove
## Bullet Point Examples (Before → After)

Rules:
- Be specific
- No generic advice
- Focus on impact, metrics, ownership
"""
    return await call_gpt_async(prompt, temperature=0.15)
