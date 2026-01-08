from agents import researcher_agent, planner_agent, writer_agent


def detect_intent(query: str) -> str:
    q = query.lower()

    if any(k in q for k in ["what is", "define", "meaning of"]):
        return "FACTUAL"

    if any(k in q for k in ["explain", "how does", "why"]):
        return "EXPLANATION"

    if any(k in q for k in ["compare", "vs", "difference between"]):
        return "COMPARISON"

    if any(k in q for k in ["plan", "itinerary", "roadmap", "strategy"]):
        return "PLANNING"

    return "CREATION"


"""
def orchestrate(query):
    MIN_LENGTH =300    
    query_lower = query.lower()

    use_research = True
    use_planning = True

    if len(query.split()) < 6:
        use_research = False

    factual_keywords = ["what is", "define", "meaning of"]
    if any(k in query_lower for k in factual_keywords):
        use_planning = False

    context = query

    if use_research:
        context = researcher_agent(context)

    if use_planning:
        context = planner_agent(context)

    final = writer_agent(context)

    retried = False
    if len(final) < MIN_LENGTH and use_planning:
        retried = True
        refined_plan = planner_agent(context + "\nImprove clarity and depth.")
        final = writer_agent(refined_plan)
#

    # ✅ ALWAYS return the same shape
    return {
        "used_research": use_research,
        "used_planning": use_planning,
        "retried": retried,
        "final": final
    }
"""

def orchestrate(query):
    intent = detect_intent(query)

    retried = False
    context = query

    if intent in ["EXPLANATION", "COMPARISON", "PLANNING"]:
        context = researcher_agent(context)

    if intent in ["COMPARISON", "PLANNING", "CREATION"]:
        context = planner_agent(context)

    final = writer_agent(context)

    return {
        "intent": intent,
        "retried": retried,
        "final": final
    }
