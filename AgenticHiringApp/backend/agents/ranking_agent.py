def rank_candidates(results):
    def ranking_key(candidate):
        return (
            candidate["decision"] == "SELECT",
            candidate["score"]
        )

    return sorted(results, key=ranking_key, reverse=True)