def route_query(query: str):
    q = query.lower().strip()

    # HARD STOP — SIMPLE QUESTIONS
    if q.startswith(("what is", "define", "explain", "meaning of")):
        return "weak", 0.0, {"reason": "hardcoded_simple"}

    # STRONG MUST BE EXPLICIT
    strong_triggers = [
        "design", "architecture", "compare", "optimize",
        "scalable", "strategy", "tradeoff"
    ]

    if not any(t in q for t in strong_triggers):
        return "weak", 0.2, {"reason": "no_strong_trigger"}

    return "strong", 0.9, {"reason": "explicit_design_intent"}
