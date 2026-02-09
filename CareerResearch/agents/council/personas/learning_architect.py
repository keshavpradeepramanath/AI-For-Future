from services.llm_router import call_all_models_async

async def learning_architect_views_async(target_role):
    prompt = f"""
You design learning paths.

Target Role: {target_role}

Provide:
- Optimal learning sequence
- Best resource types
- Common learning mistakes
"""
    return await call_all_models_async(prompt)
