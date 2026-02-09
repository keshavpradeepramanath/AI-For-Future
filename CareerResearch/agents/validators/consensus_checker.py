def check_consensus(model_outputs: dict, min_agreement: int = 2):
    """
    model_outputs example:
    {
        "GPT": "text...",
        "Gemini": "text..."
    }
    """

    signals = {}
    disagreements = []

    texts = list(model_outputs.values())

    for model, text in model_outputs.items():
        for other_text in texts:
            if model != other_text and text[:120] in other_text:
                signals[model] = signals.get(model, 0) + 1

    agreed = [m for m, count in signals.items() if count >= min_agreement]
    disagreed = [m for m in model_outputs.keys() if m not in agreed]

    return {
        "agreed_models": agreed,
        "disagreed_models": disagreed,
        "consensus_level": len(agreed)
    }
