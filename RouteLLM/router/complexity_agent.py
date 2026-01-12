# router/complexity_agent.py
import re

REASONING_KEYWORDS = [
    "design",
    "architecture",
    "tradeoff",
    "compare",
    "optimize",
    "scalable",
    "fault tolerance",
    "agentic",
    "migration",
    "governance"
]


def analyze_complexity(query: str):
    words = query.lower().split()
    word_count = len(words)

    # Length signal
    length_score = min(word_count / 40, 1.0)

    # Keyword signal
    keyword_hits = sum(1 for k in REASONING_KEYWORDS if k in query.lower())
    keyword_score = min(keyword_hits / 4, 1.0)

    # Question depth
    question_depth = query.count("?") * 0.15

    # Instruction count
    instruction_score = 0.2 if "," in query or " and " in query.lower() else 0.0

    SIMPLE_TERMS = ["what is", "define", "meaning of"]

    simple_penalty = -0.25 if any(t in query.lower() for t in SIMPLE_TERMS) else 0.0

    score = max(
        0.0,
        (
            0.35 * length_score +
            0.45 * keyword_score +
            0.20 * instruction_score +
            simple_penalty
        )
    )


    return round(score, 2), {
        "word_count": word_count,
        "length_score": round(length_score, 2),
        "keyword_hits": keyword_hits,
        "keyword_score": round(keyword_score, 2),
        "instruction_score": instruction_score,
        "question_depth": question_depth
    }
