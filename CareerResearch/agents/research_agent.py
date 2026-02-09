from services.llm_service import call_llm
from prompts.research_prompt import RESEARCH_PROMPT

def research_role(current_role, target_role, years_exp):
    prompt = RESEARCH_PROMPT.format(
        current_role=current_role,
        target_role=target_role,
        years_exp=years_exp
    )
    return call_llm(prompt)
