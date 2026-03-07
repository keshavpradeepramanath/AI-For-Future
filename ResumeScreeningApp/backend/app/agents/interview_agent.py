import json
from app.services.llm_service import call_llm


async def generate_interview_insights(jd_text, resume_text):

    prompt = f"""
You are a senior technical interviewer.

Given the Job Description and Resume:

1. Identify the candidate's strongest skill relevant to the role.
2. Identify the most important skill gap.
3. Generate ONE interview question to assess the gap.

Return JSON:

{{
 "strength": "...",
 "skill_gap": "...",
 "interview_question": "..."
}}

Job Description:
{jd_text}

Resume:
{resume_text}
"""

    response = await call_llm(prompt)

    return json.loads(response)