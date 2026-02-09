from agents.council.personas.hiring_manager import hiring_manager_views
from agents.council.personas.senior_engineer import senior_engineer_views
from agents.council.personas.career_coach import career_coach_views
from agents.council.personas.learning_architect import learning_architect_views
from agents.council.council_chair import synthesize_council

def run_multi_llm_council(current_role, target_role, years_exp):
    council_outputs = {
        "Hiring Manager": hiring_manager_views(current_role, target_role, years_exp),
        "Senior Engineer": senior_engineer_views(target_role),
        "Career Coach": career_coach_views(current_role, target_role, years_exp),
        "Learning Architect": learning_architect_views(target_role),
    }

    return synthesize_council(council_outputs)
