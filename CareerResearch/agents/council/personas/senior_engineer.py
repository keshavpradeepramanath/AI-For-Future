from services.llm_router import call_all_models_async

async def senior_engineer_views_async(target_role):
    prompt = f"""
You are a senior engineer actively working in the role: {target_role}.

Explain:
- Core technical depth required
- System design expectations
- Tooling and engineering practices
- Common mistakes less experienced engineers make

Focus on real, day-to-day work — not interview theory.
"""
    return await call_all_models_async(prompt)
