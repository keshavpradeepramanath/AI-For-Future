import asyncio

from agents.council.personas.hiring_manager import hiring_manager_views_async
from agents.council.personas.senior_engineer import senior_engineer_views_async
from agents.council.personas.career_coach import career_coach_views_async
from agents.council.personas.learning_architect import learning_architect_views_async
from agents.council.content_curator import curate_learning_content_async
from agents.council.council_chair import synthesize_council
from agents.resume.resume_parser import parse_resume
from agents.resume.resume_analyzer import analyze_resume_against_plan
from agents.resume.resume_gap_chair import generate_resume_improvements


async def _run_council_async(current_role, target_role, years_exp):
    # -----------------------------
    # Phase 1: Career Roadmap
    # -----------------------------
    hm, se, cc, la = await asyncio.gather(
        hiring_manager_views_async(current_role, target_role, years_exp),
        senior_engineer_views_async(target_role),
        career_coach_views_async(current_role, target_role, years_exp),
        learning_architect_views_async(target_role),
    )

    council_inputs = {
        "Hiring Manager": hm,
        "Senior Engineer": se,
        "Career Coach": cc,
        "Learning Architect": la,
    }

    career_prompt = f"""
You are the chair of an expert LLM council.

Below are opinions from multiple personas and models:
{council_inputs}

Your task:
- Identify agreement
- Resolve disagreements
- Produce ONE unified career roadmap

Use EXACT headings:
## Role Expectations
## Required Skillsets
## Learning Roadmap
## Career Risks & Practical Advice
"""

    career_plan = await synthesize_council(career_prompt)

    # -----------------------------
    # Phase 2: Learning Content
    # -----------------------------
    content_inputs = await curate_learning_content_async(
        target_role=target_role,
        skills=career_plan
    )

    content_prompt = f"""
You are the chair of a learning-content council.

Below are recommendations from multiple LLMs:
{content_inputs}

Your task:
- Pick the BEST content only
- Prefer high ratings (4.5+)
- Prefer large learner base (100k+)
- Remove niche or weak resources

Produce EXACTLY:

## Top Free Resources (YouTube)
1. Title – Instructor (Rating, Learners)
2. ...
3. ...

## Top Paid Resources
1. Title – Platform – Instructor (Rating, Learners)
2. ...
3. ...
"""

    content_plan = await synthesize_council(content_prompt)

    return career_plan, content_plan


def run_multi_llm_council(current_role, target_role, years_exp):
    return asyncio.run(
        _run_council_async(current_role, target_role, years_exp)
    )



async def run_resume_gap_analysis_async(uploaded_file, career_plan: str):
    resume_text = parse_resume(uploaded_file)

    gap_analysis = await analyze_resume_against_plan(
        resume_text=resume_text,
        career_plan=career_plan
    )

    improvement_plan = await generate_resume_improvements(gap_analysis)

    return gap_analysis, improvement_plan