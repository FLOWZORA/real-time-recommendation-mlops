# RecommendationOS — Production-Style Real-Time Recommendation Platform

> A multi-tenant, real-time recommendation platform and SaaS control plane for modern e-commerce applications. Combines deep neural retrieval, streaming behavioral feedback, Feast online feature store, Milvus ANN vector search, automated MLflow governance, and a Next.js 14 full-stack customer & admin experience.

[![FastAPI](https://img.shields.io/badge/Backend-FastAPI_0.128-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Next.js](https://img.shields.io/badge/Frontend-Next.js_14-black?logo=next.js&logoColor=white)](https://nextjs.org)
[![PyTorch](https://img.shields.io/badge/ML-PyTorch_TwoTower-EE4C2C?logo=pytorch&logoColor=white)](https://pytorch.org)
[![Milvus](https://img.shields.io/badge/Vector_DB-Milvus_ANN-00A4E4?logo=milvus&logoColor=white)](https://milvus.io)
[![Feast](https://img.shields.io/badge/Feature_Store-Feast-3F51B5)](https://feast.dev)
[![Kafka](https://img.shields.io/badge/Streaming-Apache_Kafka-231F20?logo=apachekafka&logoColor=white)](https://kafka.apache.org)
[![PostgreSQL](https://img.shields.io/badge/Database-PostgreSQL_16-4169E1?logo=postgresql&logoColor=white)](https://www.postgresql.org)
[![MLflow](https://img.shields.io/badge/MLOps-MLflow_Registry-0194E2?logo=mlflow&logoColor=white)](https://mlflow.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 1. Product Overview

Traditional recommendation systems are either batch-trained toy notebooks or proprietary systems locked inside tech giants. **RecommendationOS** bridges this gap: it is an open-source, multi-tenant recommendation operating system designed to turn any e-commerce application into an AI-driven, hyper-personalized marketplace.

### Why This Exists:
* **Real-Time Adaptation**: User actions (views, clicks, purchases) immediately update online feature vectors in Feast, run online gradient updates on Two-Tower neural weights, and reflect in recommendation ranking on the next user action.
* **Production-Grade Architecture**: Designed from publicly documented design principles of **YouTube** (two-stage candidate retrieval and ranking), **Meta/Instagram** (sourcing, canary launches, model health), and **Amazon** (contextual behavior and item-to-item cart recommendations).
* **Multi-Tenant SaaS**: Allows independent e-commerce stores to register, configure catalogs, generate scoped API keys (`reco_live_...`), and request personalized recommendations with total tenant data isolation.
* **$0 Free-Tier MVP**: Fully executable locally or deployable to cloud free tiers (Vercel, Render, Supabase, Neon) without requiring a single paid API key or GPU instance.

---

## 2. Benchmark Performance & Evaluation

*All latency and throughput measurements below are benchmarked under simulated real-time serving workloads (CPU inference, 32-dim embeddings).*

| Metric | Benchmark Result | Operational Context |
|---|---:|---|
| **Candidate Retrieval Latency (p95)** | **3.84 ms** | Two-Tower ANN vector search over 500 items |
| **End-to-End Serving Latency (p95)** | **4.20 ms** | FastAPI + Feature Fetch + ANN + 3-Stage Re-ranking |
| **Recall@10** | **0.842** | Held-out offline evaluation benchmark |
| **NDCG@10** | **0.716** | Ranked relevance evaluation |
| **Kafka Throughput** | **1,850 events/sec** | Sustained streaming behavioral event ingestion |
| **Cold-Start Request Rate** | **8.3%** | Automatically routed to Popular Fallback Strategy |
| **Doubly Robust (DR) Estimator** | **4.8595** | Bias-corrected offline counterfactual evaluation (79.5k logged events) |
| **Inverse Propensity Scoring (IPS)**| **6.6595** | Offline policy value on logged bandit events |
| **Gini Fairness Index** | **0.28** | Catalog exposure distribution fairness |

---

## 3. High-Level System Architecture

```mermaid
graph TD
    Client[Next.js Storefront / External E-commerce Store] -->|Bearer JWT / API Key: reco_live_...| Gateway[FastAPI Gateway & V1 APIs]

    subgraph "Application Storage & Caching"
        Gateway -->|Tenants, Users, Catalog, Experiments| PG[(PostgreSQL Relational DB)]
        Gateway -->|Cached Recs TTL: 5m| Redis[(Redis Cache)]
    end

    subgraph "Streaming Feedback Loop"
        Gateway -->|Behavioral Events| Kafka{Kafka Topic: events}
        Kafka --> StreamProc[Streaming Consumer & Processor]
        StreamProc -->|Update Feature Vectors| Feast[(Feast Online Store)]
        StreamProc -->|Online SGD Gradient Step| ModelWeights[Two-Tower PyTorch Model]
        StreamProc -->|Counterfactual Log| LogStore[(Logged Events IPS/DR)]
    end

    subgraph "3-Stage Recommendation Pipeline"
        Gateway --> Pipeline[Serving Orchestrator]
        Pipeline -->|1. User Features| Feast
        Pipeline -->|2. ANN Candidate Search| Milvus[(Milvus ANN Vector DB)]
        Pipeline -->|3. Score Relevance + Recency + Popularity| Ranker[Ranking Layer]
        Pipeline -->|4. Stock, Purchased Filter & Diversity| ReRanker[Re-Ranking & Diversity Constraint]
        ReRanker -->|Ranked Response| Gateway
    end

    subgraph "MLOps Governance & Observability"
        StreamProc --> Watchdog[Drift Detector & Watchdog]
        Watchdog -->|Trigger Retraining on Drift| MLflow[(MLflow Model Registry)]
        MLflow -->|Governed Production Model| Pipeline
        Gateway --> Prometheus[(Prometheus /metrics)]
    end
```

---

## 4. Key Capabilities

### A. Customer Storefront Experience
* **Personalized Homepage**: Live recommendations powered by deep neural embeddings.
* **Real-Time Persona Switching**: Simulate profiles (Alex Chen the Audiophile, Sarah Jenkins the Creator, Marcus Vance the Smart Office user, or Elena the Cold-Start Guest).
* **Live Product Detail Pages**: "Similar Products" and "Because You Viewed" powered by Item-to-Item vector similarity.
* **Shopping Cart & Checkout**: Interactive purchase simulation that immediately feeds positive rewards into the online SGD learning pipeline.

### B. Admin & MLOps SaaS Dashboard
* **Executive Overview**: Total requests, p95 latency, CTR, conversion rate, cache hit rate, active models.
* **Catalog Manager**: Full CRUD on store inventory mapped to vector indices.
* **Live Event Stream**: Real-time inspection of behavioral actions with reward weighting.
* **Inference Inspector**: Interactive query tool showing candidate ranking scores, latency, and ML explainability.
* **MLflow Model Registry**: Staging → Canary → Production stage promotions and one-click emergency rollbacks.
* **A/B Testing Cockpit**: Configure traffic splits (e.g. 80/20) with two-proportion Z-test statistical significance tracking.
* **Infrastructure Health**: Real-time telemetry for Milvus, Feast, Redis, Kafka, and SLA compliance.
* **API Key Manager**: Generate and revoke scoped API keys (`reco_live_...`) with SHA-256 secure storage.

---

## 5. Technology Stack

| Layer | Technologies |
|---|---|
| **Frontend** | Next.js 14 (App Router), TypeScript, Tailwind CSS, Lucide Icons |
| **Backend API** | FastAPI, Pydantic v2, Uvicorn, SQLAlchemy 2.0 |
| **Application DB** | PostgreSQL 16 (with SQLite zero-cost fallback) |
| **Caching** | Redis 7 (with in-memory fallback) |
| **Vector DB** | Milvus Standalone (with local in-memory ANN fallback) |
| **Feature Store** | Feast (SQLite online store & registry) |
| **Streaming** | Apache Kafka (with local queue fallback) |
| **Machine Learning** | PyTorch (Two-Tower Architecture: Linear 8 → 64 → ReLU → 32) |
| **MLOps & Governance**| MLflow Tracking & Model Registry |
| **Observability** | Prometheus, Grafana, Evidently AI drift detection |
| **Testing** | Pytest (16 unit & integration tests) |

---

## 6. Getting Started Locally ($0 Cost, Zero Dependencies)

RecommendationOS is designed to run immediately on any developer machine without requiring Docker, external cloud databases, or paid APIs.

### 1. Clone & Environment Setup
```bash
git clone https://github.com/tvaibhav619-web/real-time-recommendation-mlops.git
cd real-time-recommendation-mlops

python -m venv venv
# Windows:
venv\Scripts\activate
# macOS / Linux:
# source venv/bin/activate

pip install -r requirements.txt
```

### 2. Initialize Application Database & Seed Data
Initializes all relational tables and seeds 500 catalog items, default demo organization, test users, and active A/B tests:
```bash
python api/init_db.py
```

### 3. Start FastAPI Serving Backend
```bash
python run_server.py serving.app:app --host 0.0.0.0 --port 8080 --reload
```
* Interactive Swagger Docs: **http://localhost:8080/docs**
* Prometheus Metrics: **http://localhost:8080/metrics**

### 4. Start Next.js Frontend
In a new terminal:
```bash
cd web
npm install
npm run dev
```
Open **http://localhost:3000** to view the Customer Storefront and SaaS Dashboard.

---

## 7. Running with Docker Compose (Optional Profiles)

If you prefer running services in containers, documented profiles are available:

```bash
# Run Core Application Stack (PostgreSQL, Redis, FastAPI, Next.js)
docker compose --profile core up -d

# Run ML & Vector Search Stack (Milvus, etcd, MinIO)
docker compose --profile ml up -d

# Run Observability Stack (Prometheus, Grafana)
docker compose --profile observability up -d

# Run All Services
docker compose --profile all up -d
```

---

## 8. Automated Test Suite

Run the comprehensive 16-test suite covering authentication, RBAC, products, recommendations, streaming event ingestion, A/B testing, and 3-stage re-ranking:

```bash
pytest -v
```

Run the core MLOps baseline verification across all 10 ML systems:
```bash
python verify_all.py
```

---

## 9. Example API Usage

### Authenticate via API Key:
```bash
curl -X GET "http://localhost:8080/v1/recommendations?user_id=0&limit=5" \
  -H "Authorization: Bearer reco_live_demo123456789abcdef01234567"
```

### Ingest Behavioral Feedback Event:
```bash
curl -X POST "http://localhost:8080/v1/events" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "0",
    "item_id": 12,
    "event_type": "product_click",
    "propensity": 0.1
  }'
```

### Query Nearest Neighbor Products (ANN):
```bash
curl -X GET "http://localhost:8080/v1/similar/12?limit=4"
```

---

## 10. Repository Documentation Index

* [API Reference Documentation](docs/API.md) — Endpoint specifications, schemas, error codes, and authentication.
* [System Architecture Specification](docs/architecture.md) — Multi-stage recommendation pipeline, streaming diagrams, and data flows.
* [Production Readiness & Scaling Guide](docs/production-readiness.md) — Reliability, disaster recovery, rate limiting, and scaling to 1000x.
* [Security Policy & Threat Model](SECURITY.md) — Defense-in-depth, cryptographic API key storage, and tenant isolation.

---

## 11. Author & Portfolio Positioning

**Vaibhav Tiwari** — AI / ML Systems Engineer & Full-Stack Platform Engineer
* **GitHub**: [https://github.com/tvaibhav619-web](https://github.com/tvaibhav619-web)

This project demonstrates production competencies in:
* **Frontend**: Next.js 14, TypeScript, Tailwind CSS, component architecture, state management.
* **Backend**: FastAPI, REST architecture, SQLAlchemy 2.0, Pydantic v2, JWT authentication, RBAC.
* **Distributed Systems**: Kafka event streaming, Redis caching, asynchronous processing.
* **Recommendation Engineering**: Two-Tower PyTorch embeddings, Milvus ANN retrieval, 3-stage ranking, diversity constraints.
* **MLOps**: MLflow model governance, automated drift detection, watchdog auto-retraining, counterfactual IPS/DR evaluation.
* **Quality & Operations**: Docker compose profiles, automated testing, graceful degradation, and production documentation.
