# agents/critic_agent.py
def critique(answer, query):
    if len(answer.split()) < 50:
        return "ESCALATE"
    if "I don't know" in answer.lower():
        return "ESCALATE"
    return "PASS"
