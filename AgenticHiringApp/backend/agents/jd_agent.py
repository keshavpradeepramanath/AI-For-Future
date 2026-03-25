from services.llm import call_llm

def parse_jd(jd_text):
    prompt = f"""
    Extract key information from this job description.

    Return:

    Role: <job title>
    Skills: <comma separated>
    Experience: <years>

    JD:
    {jd_text[:12000]}
    """

    return call_llm(prompt)
