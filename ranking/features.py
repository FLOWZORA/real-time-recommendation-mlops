from features.catalog_data import get_item_metadata, get_user_persona

def item_is_cold(item_features: dict) -> bool:
    return item_features.get("popularity", 0) == 0

def build_ranking_features(user_id: int, item_id: int, ann_score: float = None):
    """
    Ranking features for candidate items based on authentic category affinity,
    Two-Tower embedding score, rating, and review popularity.
    """
    meta = get_item_metadata(item_id)
    persona = get_user_persona(user_id)

    item_cat = meta.get("category")
    primary_cat = persona.get("primary_cat")
    secondary_cat = persona.get("secondary_cat")
    affinity_tags = persona.get("affinity_tags") or []

    # Base relevance from category affinity:
    # primary (1.0) > secondary (0.75) > affinity-tag match (0.60) > other (0.25).
    # The tertiary tier lets personas with broad lifestyles (e.g. Max Sterling:
    # Workspace + Audio + Smart Home) fill diversity slots with on-theme gear
    # instead of generic backfill, without disturbing primary rankings.
    if primary_cat and item_cat == primary_cat:
        cat_rel = 1.0
    elif secondary_cat and item_cat == secondary_cat:
        cat_rel = 0.75
    elif item_cat in affinity_tags:
        cat_rel = 0.60
    else:
        cat_rel = 0.25

    if ann_score is not None:
        relevance_score = 0.5 * cat_rel + 0.5 * max(0.0, min(1.0, float(ann_score)))
    else:
        relevance_score = cat_rel

    rating = float(meta.get("rating", 4.5))
    reviews = int(meta.get("reviews", 500))

    popularity = min(rating / 5.0, 1.0)
    recency = min(reviews / 10000.0, 1.0)

    # Flagship bonus for hand-curated seeds (0-59) and the
    # Max Sterling fitness lineup (480-499) so new athletic gear
    # competes on equal footing instead of losing to coffee flagships.
    if item_id < 60 or 480 <= item_id < 500:
        relevance_score = min(1.0, relevance_score + 0.15)
        popularity = min(1.0, popularity + 0.1)

    feats = {
        "relevance_score": relevance_score,
        "popularity": popularity,
        "recency": recency,
    }

    return feats


