from services.llm import call_llm

def screen_candidate_multi(jds, resume):
    """
    Evaluate resume against ALL JDs in ONE LLM call
    """

    jd_block = ""

    for i, jd in enumerate(jds):
        jd_block += f"""
        JD {i+1} ({jd['name']}):
        {str(jd['content'])[:1500]}
        """

    prompt = f"""
    You are an expert recruiter.

    Evaluate the candidate against MULTIPLE job descriptions.

    IMPORTANT:
    - Compare candidate with ALL JDs
    - Select the BEST matching JD
    - Be fair and not overly strict
    - Detect skills properly

    SCORING GUIDE:
    - Strong → 70–90
    - Moderate → 50–70
    - Weak → <40

    Return EXACT format:

    Matched JD: <JD file name>
    Score: <0-100>
    Decision: <SELECT or REJECT>
    Reasoning: <2-3 lines>
    Summary: <50 word profile summary>

    ======================
    JOB DESCRIPTIONS:
    {jd_block}

    ======================
    RESUME:
    {resume[:4000]}
    """

    return call_llm(prompt)