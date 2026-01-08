from agents import researcher_agent, planner_agent, writer_agent
import time

"""
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
"""



MIN_LENGTH = 150


def detect_intent(query: str) -> str:
    q = query.lower()

    if any(k in q for k in ["what is", "define", "meaning of"]):
        return "FACTUAL"

    if any(k in q for k in ["explain", "how does", "why"]):
        return "EXPLANATION"

    if any(k in q for k in ["compare", "vs", "difference"]):
        return "COMPARISON"

    if any(k in q for k in ["plan", "itinerary", "roadmap", "strategy"]):
        return "PLANNING"

    return "CREATION"

"""
def orchestrate(query):
    intent = detect_intent(query)
    trace = []
    retried = False

    # ⚡ FAST PATH (new)
    if intent == "FACTUAL":
        trace.append("writer")
        final = writer_agent(query)
        return {
            "intent": intent,
            "trace": trace,
            "retried": False,
            "final": final
        }

    context = query

    # 🔍 Research
    trace.append("researcher")
    context = researcher_agent(context)

    # 🧠 Planning (only when useful)
    if intent in ["COMPARISON", "PLANNING", "CREATION"]:
        trace.append("planner")
        context = planner_agent(context)

    # ✍️ Writing
    trace.append("writer")
    final = writer_agent(context)

    # 🔁 Controlled retry
    if intent in ["PLANNING", "COMPARISON"] and len(final) < MIN_LENGTH:
        retried = True
        trace.append("retry_planner")
        refined = planner_agent(context + "\nImprove clarity and depth.")
        trace.append("retry_writer")
        final = writer_agent(refined)

    return {
        "intent": intent,
        "trace": trace,
        "retried": retried,
        "final": final
    }

"""



def timed(agent_name, fn, arg, trace):
    start = time.time()
    result = fn(arg)
    duration = int((time.time() - start) * 1000)
    trace.append({"agent": agent_name, "ms": duration})
    return result


def calculate_confidence(final_text, trace):
    score = 0.5

    if len(final_text) > 300:
        score += 0.2
    if final_text.count("\n") > 5:
        score += 0.1
    if len(trace) <= 2:
        score += 0.1

    return min(round(score, 2), 0.95)



def orchestrate(query):
    intent = detect_intent(query)
    trace = []
    retried = False

    # ⚡ FAST PATH
    if intent == "FACTUAL":
        final = timed("writer", writer_agent, query, trace)
        confidence = calculate_confidence(final, trace)
        return {
            "intent": intent,
            "trace": trace,
            "retried": False,
            "confidence": confidence,
            "final": final
        }

    context = query

    context = timed("researcher", researcher_agent, context, trace)

    if intent in ["COMPARISON", "PLANNING", "CREATION"]:
        context = timed("planner", planner_agent, context, trace)

    final = timed("writer", writer_agent, context, trace)

    confidence = calculate_confidence(final, trace)

    return {
        "intent": intent,
        "trace": trace,
        "retried": retried,
        "confidence": confidence,
        "final": final
    }