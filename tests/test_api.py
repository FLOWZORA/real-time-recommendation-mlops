import pytest
from fastapi.testclient import TestClient
from serving.app import app

client = TestClient(app)

def test_health():
    res = client.get("/health")
    assert res.status_code == 200
    assert res.json()["status"] == "ok"

def test_auth_login():
    res = client.post("/v1/auth/login", json={
        "email": "admin@recommendationos.io",
        "password": "AdminPassword123!"
    })
    assert res.status_code == 200
    data = res.json()
    assert "access_token" in data
    assert data["role"] == "STORE_ADMIN"

def test_products_list():
    res = client.get("/v1/products?limit=5")
    assert res.status_code == 200
    products = res.json()
    assert len(products) == 5
    assert "title" in products[0]
    assert "price" in products[0]

def test_recommendation_v1_query():
    # Cold user
    res_cold = client.get("/v1/recommendations?user_id=cold_user_999999")
    assert res_cold.status_code == 200
    data_cold = res_cold.json()
    assert data_cold["cold_start"] is True
    assert len(data_cold["recommendations"]) == 10

    # Warm user (user 0)
    res_warm = client.get("/v1/recommendations?user_id=0")
    assert res_warm.status_code == 200
    data_warm = res_warm.json()
    assert data_warm["cold_start"] is False
    assert len(data_warm["recommendations"]) == 10

def test_similar_products():
    res = client.get("/v1/similar/10?limit=4")
    assert res.status_code == 200
    sim = res.json()
    assert len(sim) == 4
    assert sim[0]["item_id"] != 10

def test_event_ingestion():
    res = client.post("/v1/events", json={
        "user_id": "test_user_42",
        "item_id": 12,
        "event_type": "product_view"
    })
    assert res.status_code == 200
    ev = res.json()
    assert ev["user_id"] == "test_user_42"
    assert ev["item_id_numeric"] == 12

def test_analytics_overview():
    res = client.get("/v1/analytics/overview")
    assert res.status_code == 200
    overview = res.json()
    assert overview["total_products"] >= 500
    assert "overall_ctr" in overview
    assert "avg_latency_ms" in overview

def test_api_keys_with_bearer():
    # Login as admin to get token
    login_res = client.post("/v1/auth/login", json={
        "email": "admin@recommendationos.io",
        "password": "AdminPassword123!"
    })
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # List keys
    list_res = client.get("/v1/api-keys", headers=headers)
    assert list_res.status_code == 200

    # Create new key
    create_res = client.post("/v1/api-keys", json={"name": "Test Key"}, headers=headers)
    assert create_res.status_code == 201
    created_key = create_res.json()
    assert "secret_key" in created_key
    assert created_key["secret_key"].startswith("reco_live_")

    # Use the generated API key to access recommendations
    key_auth_res = client.get(
        "/v1/recommendations?user_id=99",
        headers={"Authorization": f"Bearer {created_key['secret_key']}"}
    )
    assert key_auth_res.status_code == 200
