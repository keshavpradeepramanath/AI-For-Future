import json
from app.services.llm_service import call_llm


async def screen_resume(jd_text, resume_text):

    prompt = f"""
You are an expert recruiter.

Evaluate how well the resume matches the job description.

Return STRICT JSON:

{{
 "candidate_name": "Name of the candidate",
 "score": number between 0 and 100,
 "decision": "Selected or Not Selected",
 "reason": "2 short sentences explaining the decision"
}}

Scoring guidelines:
90-100 = Excellent match
70-89 = Strong match
50-69 = Moderate match
Below 50 = Poor match

Job Description:
{jd_text}

Resume:
{resume_text}
"""

    response = await call_llm(prompt)

    data = json.loads(response)

    return {
        "candidate_name": data.get("candidate_name", "Unknown Candidate"),
        "score": data.get("score", 0),
        "decision": data.get("decision", "Not Selected"),
        "reason": data.get("reason", "No explanation available")
    }
