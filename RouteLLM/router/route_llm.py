def route_query(query: str) -> str:
    q = query.lower().strip()

    # Simple definitions → WEAK
    if q.startswith(("what is", "define", "explain", "meaning of")):
        return "weak"

    # Design / architecture / comparison → STRONG
    STRONG_TERMS = [
        "design",
        "architecture",
        "compare",
        "optimization",
        "optimize",
        "strategy",
        "routing",
        "system"
    ]

    for term in STRONG_TERMS:
        if term in q:
            return "strong"

    # Default → WEAK
    return "weak"
