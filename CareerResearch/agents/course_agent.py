from services.llm_service import call_llm
from prompts.course_prompt import COURSE_PROMPT

def recommend_courses(skills, target_role):
    prompt = COURSE_PROMPT.format(
        skills=skills,
        target_role=target_role
    )
    return call_llm(prompt)
