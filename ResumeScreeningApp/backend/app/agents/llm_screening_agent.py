import json
from app.services.llm_service import call_llm


async def evaluate_candidate(jd_text, resume_text):

    prompt = f"""
You are a strict senior technical hiring manager.

Evaluate the candidate resume against the job description.

Scoring rubric:

Technical skill match: 40
Relevant experience: 30
Project relevance: 20
Tool alignment: 10

Return JSON:

{{
"candidate_name":"Candidate",
"score":number,
"decision":"Selected or Not Selected",
"reason":"short explanation",
"strength":"main strength",
"skill_gap":"main gap"
}}

Job Description:
{jd_text}

Resume:
{resume_text}
"""

    response = await call_llm(prompt)

    try:
        return json.loads(response)
    except:
        return {
            "candidate_name": "Candidate",
            "score": 0,
            "decision": "Not Selected",
            "reason": "LLM parsing failed",
            "strength": "",
            "skill_gap": ""
        }