import re

WEAK_ALLOWLIST = [
    r"^what is\b",
    r"^define\b",
    r"^explain\b",
    r"^meaning of\b",
    r"^who is\b",
    r"^when\b",
    r"^where\b"
]

def force_weak(query: str) -> bool:
    q = query.lower().strip()
    return any(re.match(p, q) for p in WEAK_ALLOWLIST)


STRONG_TRIGGERS = [
    "design",
    "architecture",
    "tradeoff",
    "compare",
    "optimize",
    "scalable",
    "fault tolerance",
    "migration",
    "strategy",
    "agentic",
]

def has_strong_signal(query: str) -> bool:
    q = query.lower()
    return any(t in q for t in STRONG_TRIGGERS)
