from services.llm_service import call_llm
from prompts.skill_prompt import SKILL_PROMPT

def extract_skills(role_research):
    prompt = SKILL_PROMPT.format(role_research=role_research)
    return call_llm(prompt)
