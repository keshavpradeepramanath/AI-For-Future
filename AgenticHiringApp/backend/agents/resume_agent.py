from services.llm import call_llm
def parse_resume(resume_text):
    prompt = f"""
    Summarize this job description into structured JSON.

    Keep it SHORT and relevant.

    {{
      "role": "",
      "must_have_skills": [],
      "good_to_have_skills": [],
      "experience_required": "",
      "key_responsibilities": []
    }}

    JD:
    {resume_text[:15000]}  # 🔥 truncate
    """

    return call_llm(prompt)