import re

HALLUCINATION_PATTERNS = [
    r"guarantee",
    r"100%",
    r"always",
    r"never fail",
    r"best in the world",
    r"undisputed"
]

def detect_hallucination(text: str):
    hits = []

    for pattern in HALLUCINATION_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            hits.append(pattern)

    return {
        "hallucination_risk": len(hits) > 0,
        "patterns_found": hits
    }
