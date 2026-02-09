from services.llm_router import call_all_models

def career_coach_views(current_role, target_role, years_exp):
    prompt = f"""
You are a pragmatic career coach.

Candidate:
- Current Role: {current_role}
- Experience: {years_exp}
- Target Role: {target_role}

Advise on:
- Skill gaps
- Transition risks
- What to prioritize
"""
    return call_all_models(prompt)
