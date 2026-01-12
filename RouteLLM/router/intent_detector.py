import re

SIMPLE_REGEX = [
    r"^what is\b",
    r"^define\b",
    r"^meaning of\b",
    r"^explain\b",
]

def is_simple_question(query: str) -> bool:
    q = query.lower().strip()
    if len(q.split()) > 10:
        return False

    return any(re.match(pattern, q) for pattern in SIMPLE_REGEX)
