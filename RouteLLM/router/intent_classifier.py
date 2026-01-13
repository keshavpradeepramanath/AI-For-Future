def classify_intent(query: str) -> str:
    q = query.lower()

    if q.startswith(("what is", "define", "explain")):
        return "general"

    if any(k in q for k in [
        "design", "architecture", "compare",
        "optimize", "scalable"
    ]):
        return "design"

    if any(k in q for k in [
        "solve", "equation", "derivative", "integral"
    ]):
        return "math"

    if any(k in q for k in [
        "code", "python", "java", "bug", "implement"
    ]):
        return "coding"

    return "general"
