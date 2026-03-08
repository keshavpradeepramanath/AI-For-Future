import json
from app.services.llm_service import call_llm


async def extract_skills(resume_text):

    prompt = f"""
Extract the technical skills from this resume.

Return JSON:

{{
"skills": ["skill1","skill2","skill3"]
}}

Resume:
{resume_text}
"""

    response = await call_llm(prompt)

    try:
        return json.loads(response)["skills"]
    except:
        return []