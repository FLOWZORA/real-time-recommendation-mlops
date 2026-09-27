def rank_items(candidates):
    """
    Ranks candidate items based on combined neural relevance, popularity, and recency.
    """
    def score(x):
        return (
            0.70 * x.get("relevance_score", 0.5)
            + 0.20 * x.get("popularity", 0.5)
            + 0.10 * x.get("recency", 0.5)
        )

    return sorted(candidates, key=score, reverse=True)

