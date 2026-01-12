from router.route_llm import route_query

def test_simple_definitions():
    cases = [
        "What is LLM?",
        "Define embeddings",
        "Define embeddings in NLP",
        "Explain transformers"
    ]

    for q in cases:
        route, _, _ = route_query(q)
        assert route == "weak", f"FAILED for: {q}"
