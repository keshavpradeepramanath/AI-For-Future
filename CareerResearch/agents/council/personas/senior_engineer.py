from services.llm_router import call_all_models

def senior_engineer_views(target_role):
    prompt = f"""
You are a senior engineer in the role: {target_role}

Explain:
- Core technical depth required
- System design expectations
- Daily responsibilities
- Common mistakes
"""
    return call_all_models(prompt)
