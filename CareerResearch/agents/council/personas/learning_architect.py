from services.llm_router import call_all_models

def learning_architect_views(target_role):
    prompt = f"""
You design learning paths.

Target Role: {target_role}

Provide:
- Optimal learning sequence
- Best resource types
- Common learning mistakes
"""
    return call_all_models(prompt)
