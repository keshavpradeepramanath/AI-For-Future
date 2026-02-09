from services.llm_clients.openai_client import call_gpt_async

async def analyze_resume_against_plan(resume_text: str, career_plan: str) -> str:
    prompt = f"""
You are a senior hiring manager reviewing a resume.

CAREER TARGET (Council-approved):
{career_plan}

CANDIDATE RESUME:
{resume_text}

Task:
1. Identify missing skills vs target role
2. Identify weak or unclear experience
3. Identify resume red flags
4. Identify strengths already aligned

Use EXACT sections:

## Strong Signals
## Skill Gaps
## Experience Gaps
## Resume Issues
"""
    return await call_gpt_async(prompt, temperature=0.2)
