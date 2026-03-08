import json

from app.services.llm_service import call_llm
from app.services.cache_service import (
    generate_cache_key,
    get_cached_result,
    store_cached_result
)


async def evaluate_candidate(jd_text, resume_text):

    cache_key = generate_cache_key(jd_text, resume_text)

    cached = get_cached_result(cache_key)

    if cached:
        return cached

    prompt = f"""
You are a strict senior technical hiring manager.

Evaluate the resume against the job description.

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
"skill_gap":"main gap",
"skills":["skill1","skill2"]
}}

Job Description:
{jd_text}

Resume:
{resume_text}
"""

    response = await call_llm(prompt)

    try:

        result = json.loads(response)

        store_cached_result(cache_key, result)

        return result

    except:

        return {
            "candidate_name": "Candidate",
            "score": 0,
            "decision": "Not Selected",
            "reason": "LLM parsing failed",
            "strength": "",
            "skill_gap": "",
            "skills": []
        }