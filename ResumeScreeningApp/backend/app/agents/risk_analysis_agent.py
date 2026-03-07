import json
from app.services.llm_service import call_llm


async def analyze_risk(jd_text, resume_text):

    prompt = f"""
You are an AI fairness reviewer in a hiring system.

Analyze the candidate resume against the job description.

Identify if the candidate may be incorrectly rejected due to:

- weak English
- poor resume formatting
- missing project descriptions
- career gaps
- unconventional background

Return STRICT JSON:

{{
 "risk_level": "Low Risk | Medium Risk | High Risk",
 "risk_reason": "1-2 sentences explaining the risk",
 "recommendation": "Proceed | Human Review Recommended"
}}

Job Description:
{jd_text}

Resume:
{resume_text}
"""

    response = await call_llm(prompt)

    data = json.loads(response)

    return {
        "risk_level": data.get("risk_level", "Unknown"),
        "risk_reason": data.get("risk_reason", ""),
        "recommendation": data.get("recommendation", "")
    }
