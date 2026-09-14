import sys
import os
from pathlib import Path

# Ensure repo root is in python path
repo_root = Path(__file__).resolve().parent
if str(repo_root) not in sys.path:
    sys.path.insert(0, str(repo_root))

import torch
import numpy as np

def run_tests():
    print("==================================================")
    print("   REAL-TIME RECOMMENDATION MLOPS SYSTEM TESTS    ")
    print("==================================================")
    passed = 0
    total = 0

    def assert_test(name, condition, extra=""):
        nonlocal passed, total
        total += 1
        if condition:
            passed += 1
            print(f"[PASS] {name} {extra}")
        else:
            print(f"[FAIL] {name} {extra}")
            raise AssertionError(f"Test failed: {name}")

    # 1. Model architecture & loading
    print("\n--- 1. Two-Tower Model ---")
    from retrieval.two_tower import TwoTower
    from serving.model_loader import model

    u = torch.rand(4, 8)
    i = torch.rand(4, 8)
    out = model(u, i)
    assert_test("Model inference shape", out.shape == torch.Size([4]))
    assert_test("Model user tower", model.user(u).shape == torch.Size([4, 32]))
    assert_test("Model item tower", model.item(i).shape == torch.Size([4, 32]))

    # 2. Feature store retrieval
    print("\n--- 2. Feast Feature Store ---")
    from serving.user_features import get_user_features

    warm_feats, warm_cold = get_user_features(0)
    assert_test("Warm user features tensor", warm_feats.shape == torch.Size([1, 8]))
    assert_test("Warm user cold flag", warm_cold is False)

    cold_feats, cold_cold = get_user_features(999999)
    assert_test("Cold user features tensor", cold_feats.shape == torch.Size([1, 8]))
    assert_test("Cold user cold flag", cold_cold is True)

    # 3. Vector database & ANN search
    print("\n--- 3. Vector Database (Milvus / Local Fallback) ---")
    from vector_db.milvus import search, insert_embeddings

    test_vectors = np.random.rand(50, 32).astype(np.float32)
    insert_embeddings(test_vectors)
    query_vec = test_vectors[0]
    hits = search(query_vec, top_k=5)
    assert_test("Vector search returns top_k items", len(hits) == 5)
    assert_test("Vector search best match is item 0", hits[0] == 0)

    # Reload full 500 items embeddings
    if (repo_root / "item_embeddings.npy").exists():
        insert_embeddings(np.load(repo_root / "item_embeddings.npy"))

    # 4. Ranking & Exploration
    print("\n--- 4. Ranking & Exploration ---")
    from ranking.features import build_ranking_features
    from ranking.ranker import rank_items

    f1 = build_ranking_features(1, 10)
    assert_test("Build ranking features contains required keys",
                all(k in f1 for k in ["relevance_score", "popularity", "recency"]))
    candidates = [
        {"item_id": 1, "relevance_score": 0.9, "popularity": 5, "recency": 0.5},
        {"item_id": 2, "relevance_score": 0.1, "popularity": 1, "recency": 0.1},
    ]
    ranked = rank_items(candidates)
    assert_test("Rank items orders by score descending", ranked[0]["item_id"] == 1)

    # 5. Cold start handler
    print("\n--- 5. Cold Start Recommendation ---")
    from cold_start.handler import cold_start_recommend
    cs_res = cold_start_recommend(42)
    assert_test("Cold start returns popular fallback strategy", cs_res["strategy"] == "popular_fallback")
    assert_test("Cold start recommendations length", len(cs_res["items"]) == 10)

    # 6. Serving API endpoints
    print("\n--- 6. FastAPI Serving Endpoints ---")
    from fastapi.testclient import TestClient
    from serving.app import app

    client = TestClient(app)

    res_health = client.get("/health")
    assert_test("GET /health status 200", res_health.status_code == 200 and res_health.json()["status"] == "ok")

    res_metrics = client.get("/metrics")
    assert_test("GET /metrics status 200", res_metrics.status_code == 200 and len(res_metrics.text) > 0)

    res_rec_warm = client.get("/recommend/0")
    assert_test("GET /recommend/0 status 200", res_rec_warm.status_code == 200)
    data_warm = res_rec_warm.json()
    assert_test("Warm user recommendations not cold", data_warm["cold_start"] is False)
    assert_test("Warm user recommendations length", len(data_warm["recommendations"]) == 10)

    res_rec_cold = client.get("/recommend/999999")
    assert_test("GET /recommend/999999 status 200", res_rec_cold.status_code == 200)
    data_cold = res_rec_cold.json()
    assert_test("Cold user recommendations cold_start is True", data_cold["cold_start"] is True)

    # 7. Monitoring & Drift
    print("\n--- 7. Monitoring, Drift & Fairness ---")
    from monitoring.drift_detector import set_baseline, detect_drift
    from monitoring.drift_stats import log_feature, log_reward
    from monitoring.fairness import gini
    from monitoring.sla import check_latency

    set_baseline(np.zeros(8), 1.0)
    for _ in range(5):
        log_feature(np.zeros(8))
        log_reward(1.0)
    assert_test("Drift check without drift", detect_drift() is False)

    # Inject data drift
    for _ in range(20):
        log_feature(np.ones(8) * 10.0)
    assert_test("Drift check detects data drift", detect_drift() is True)

    # Fairness Gini
    assert_test("Gini perfect equality", gini([5, 5, 5, 5]) == 0.0)
    assert_test("Gini inequality", gini([0, 0, 0, 100]) == 0.75)

    # SLA check
    assert_test("SLA check acceptable latency", check_latency(0.05) is True)
    assert_test("SLA check violation", check_latency(0.15) is False)

    # 8. Counterfactual Evaluation
    print("\n--- 8. Counterfactual Offline Evaluation ---")
    from evaluation.ips import ips
    from evaluation.dr import doubly_robust

    log_path = repo_root / "evaluation" / "logged_events.jsonl"
    ips_val = ips(log_path)
    dr_val = doubly_robust(log_path)
    assert_test("IPS evaluation returns positive score", ips_val > 0, f"(Score: {ips_val:.4f})")
    assert_test("DR evaluation returns positive score", dr_val > 0, f"(Score: {dr_val:.4f})")

    # 9. Online Learning Update
    print("\n--- 9. Online Learning ---")
    from model.online_update import online_update

    loss = online_update(model, torch.rand(1, 8), torch.rand(1, 8), label=1.0)
    assert_test("Online update loss calculated", loss > 0, f"(Loss: {loss:.4f})")

    # 10. Streaming Pipeline
    print("\n--- 10. Streaming Pipeline Simulation ---")
    from streaming.producer import produce_events
    from streaming.consumer import consume_events

    produce_events(count=3, interval=0)
    consumed = consume_events(max_messages=3)
    assert_test("Streaming consumer processed produced messages", consumed == 3)

    print("\n==================================================")
    print(f"   ALL TESTS PASSED! ({passed}/{total})")
    print("==================================================")

if __name__ == "__main__":
    run_tests()
