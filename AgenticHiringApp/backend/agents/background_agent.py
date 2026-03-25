from services.llm import call_llm

def background_check(resume):
    prompt = f"""
    You are a background verification assistant.

    Analyze the candidate profile and check for consistency.

    Simulate a LinkedIn-style verification:

    Return:

    Verification: <VERIFIED / PARTIALLY VERIFIED / NOT VERIFIED>
    Confidence: <0-100>
    Risk Flags: <any inconsistencies or suspicious claims>
    Summary: <short explanation>

    Candidate Profile:
    {resume[:4000]}
    """

    return call_llm(prompt)