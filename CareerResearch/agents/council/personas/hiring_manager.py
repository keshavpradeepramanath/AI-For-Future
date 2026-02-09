from services.llm_router import call_all_models_async

async def hiring_manager_views_async(current_role, target_role, years_exp):
    prompt = f"""
You are a hiring manager.

Candidate:
- Current Role: {current_role}
- Years of Experience: {years_exp}
- Target Role: {target_role}

Provide:
- Must-have skills
- Common rejection reasons
- Strong hiring signals
"""
    return await call_all_models_async(prompt)
