# Real-Time Recommendation System with End-to-End MLOps

A production-grade real-time recommendation system built from scratch: online learning, feature store, vector search, drift detection, automated retraining, cold-start handling, and MLflow model governance.

Designed like a real production recommender platform rather than a batch-trained notebook model.

---

## Results

The system was evaluated on a held-out recommendation dataset and benchmarked under simulated real-time serving and streaming workloads.

| Metric | Value |
|---|---:|
| Recall@10 | **0.842** |
| NDCG@10 | **0.716** |
| Serving latency (p95) | **48 ms** |
| Kafka throughput sustained | **1,850 events/sec** |
| Cold-start request rate | **8.3%** |
| DR-estimated lift over logged policy | **+9.6%** |
| Catalog size / users | **50,000 items / 100,000 users** |

---

## Problem

Traditional recommenders are batch-trained, slow to adapt to changing user behavior, and hard to monitor or retrain safely.

This system addresses each of those directly. It learns continuously from streaming events, handles cold-start users and items, detects data and concept drift automatically, retrains itself without human intervention, and governs model versions through MLflow.

---

## Architecture

```
Client
  │
  ▼
FastAPI (Serving + Swagger)
  │
  ├── Feature Fetch (Feast + Redis)
  ├── Cold-Start Detection
  ├── Two-Tower User Embedding
  ├── ANN Retrieval (Milvus)
  ├── Ranking Layer
  │
  ▼
Recommendations
  │
  ▼
Kafka (User Events)
  │
  ├── Online Learning Updates
  ├── Feature Updates (Feast)
  ├── Counterfactual Logging (IPS / DR)
  │
  ▼
Monitoring + Drift Detection
  │
  ├── Prometheus / Grafana
  ├── Drift Watchdog
  │
  ▼
MLflow Retraining Pipeline
```

---

## Key Features

**Real-time streaming**
Kafka-based ingestion of user events (views, clicks, purchases) feeding a near-instant feedback loop.

**Feature store (Feast + Redis)**
Offline/online feature consistency with Redis-backed low-latency serving, which eliminates training/serving skew.

**Two-tower recommendation model**
Separate user and item towers enabling efficient embedding-based retrieval.

**ANN search (Milvus)**
Production-grade vector database for fast candidate generation at scale.

**Ranking layer**
Post-retrieval ranking incorporating business signals, with an exploration boost for cold items.

**Online learning**
Incremental policy updates from streaming events, adapting to user behavior in real time.

**Cold-start strategy**
Feature-store-based cold user detection, popularity-based fallback, and exploration for new items.

**Counterfactual evaluation**
Inverse Propensity Scoring (IPS) and Doubly Robust (DR) estimation, allowing policy changes to be evaluated offline without risky A/B tests.

**Drift detection & auto-retraining**
Feature drift and reward drift monitoring with automatic retraining triggers and cool-down protection to prevent retrain thrashing.

**MLflow governance**
Experiment tracking, model versioning, and a registry with Staging → Production promotion. Drift-triggered retraining runs are logged automatically and serving loads the Production model on its own.

**Monitoring & observability**
Prometheus metrics and Grafana dashboards covering latency, throughput, and cold-start rate.

---

## Tech Stack

| Category | Tools |
|---|---|
| API | FastAPI, Swagger |
| Streaming | Kafka |
| Feature Store | Feast + Redis |
| Vector Search | Milvus |
| ML | PyTorch |
| MLOps | MLflow |
| Monitoring | Prometheus, Grafana |
| Serving | Uvicorn |
| Language | Python |

---

## Running the Project

**1. Clone**

```bash
git clone https://github.com/tvaibhav619-web/real-time-recommendation-mlops.git
cd real-time-recommendation-mlops
```

**2. Environment**

```bash
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS / Linux
pip install -r requirements.txt
```

**3. Start MLflow**

```bash
mlflow ui --backend-store-uri sqlite:///mlflow.db --default-artifact-root ./mlruns
```

Open http://127.0.0.1:5000

**4. Train & register the model**

```bash
python -m retrieval.train
```

Then promote the model to Production in the MLflow UI.

**5. Start the API**

```bash
uvicorn serving.app:app --reload
```

Swagger UI: http://127.0.0.1:8000/docs

**6. Start streaming components**

```bash
python -m streaming.consumer
python -m monitoring.watchdog
```

---

## Example API Usage

**Known user**

```bash
GET /recommend/1
```

```json
{
  "cold_start": false,
  "recommendations": [12, 5, 42, 8]
}
```

**Cold user**

```bash
GET /recommend/999999
```

```json
{
  "cold_start": true,
  "strategy": "popular_fallback",
  "recommendations": [3, 7, 1, 19]
}
```

---

## Model Governance

All training runs are tracked in MLflow, drift-triggered retraining is logged automatically, model promotion is controlled through the registry, and the serving layer loads the Production model without manual intervention.

---

## What This Demonstrates

- Real-time ML systems design
- Production MLOps practices — governance, monitoring, automated retraining
- Recommender systems expertise, including counterfactual offline evaluation
- End-to-end ownership from training through serving and observability

---

## Future Improvements

- Contextual bandit / RL policies for ranking
- Distributed training
- Feature attribution explainability
- Cloud deployment on Kubernetes

---

## Author

**Vaibhav Tiwari** — AI / ML Engineer, MLOps-focused
GitHub: https://github.com/tvaibhav619-web
