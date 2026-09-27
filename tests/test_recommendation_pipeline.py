import pytest
from serving.pipeline import recommendation_pipeline
from api.database import SessionLocal
from api.models.product import Product

def test_pipeline_cold_start():
    # Cold user with no Feast history
    res = recommendation_pipeline.generate_recommendations(
        user_id_raw="cold_user_99999",
        organization_id="demo-store",
        top_k=10,
        enable_cache=False,
    )
    assert res["cold_start"] is True
    assert res["strategy"] == "popular_fallback"
    assert len(res["recommendations"]) == 10
    assert len(res["detailed_recommendations"]) == 10

def test_pipeline_warm_user():
    # Warm user with Feast history (user 0)
    res = recommendation_pipeline.generate_recommendations(
        user_id_raw="0",
        organization_id="demo-store",
        top_k=10,
        enable_cache=False,
    )
    assert res["cold_start"] is False
    assert res["strategy"] == "two_tower_milvus"
    assert len(res["recommendations"]) == 10
    assert res["latency_ms"] < 200  # Latency under SLA target

def test_pipeline_category_diversity():
    res = recommendation_pipeline.generate_recommendations(
        user_id_raw="0",
        organization_id="demo-store",
        top_k=10,
        enable_cache=False,
    )
    categories = [item["category"] for item in res["detailed_recommendations"]]
    cat_counts = {}
    for c in categories:
        cat_counts[c] = cat_counts.get(c, 0) + 1
    # Diversity contract mirrors serving/pipeline.py: primary affinity
    # category up to 6 items (theme depth), all other categories up to 4.
    # User 0 (Alex Chen) has primary_cat "Audio & Sound".
    for c, count in cat_counts.items():
        limit = 6 if c == "Audio & Sound" else 4
        assert count <= limit, f"Category {c} exceeded diversity limit with {count} items"

def test_pipeline_purchased_item_exclusion():
    excluded = [12, 5]
    res = recommendation_pipeline.generate_recommendations(
        user_id_raw="0",
        organization_id="demo-store",
        top_k=10,
        enable_cache=False,
        excluded_item_ids=excluded,
    )
    for excluded_id in excluded:
        assert excluded_id not in res["recommendations"], f"Item {excluded_id} was not excluded"
