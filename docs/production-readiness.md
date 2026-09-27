# RecommendationOS — Production Readiness & Scaling Guide

This document outlines the production-readiness posture of RecommendationOS, operational procedures, reliability controls, and the evolution path from a $0 free-tier MVP to high-scale commercial operations.

---

## 1. Production Readiness Checklist

### Scalability
- [x] Stateless FastAPI serving layer capable of horizontal autoscaling behind reverse proxy or Kubernetes Ingress.
- [x] Vector ANN search with $O(\log N)$ retrieval complexity via Milvus IVF_FLAT / HNSW indexing.
- [x] Asynchronous, non-blocking behavioral event ingestion using background tasks and Kafka message queues.
- [x] Redis caching layer with bounded TTLs (60s personalized, 300s popular) mitigating database load under traffic spikes.

### Reliability & Resilience
- [x] 4-Tier Fallback Degradation: Cache → Two-Tower ANN → Category Recs → Global Popular Fallback.
- [x] Hard timeout constraints on external lookups (0.5s max serving timeout).
- [x] In-memory fallbacks for all distributed components (Milvus, Redis, Kafka) ensuring zero crash-loops in degraded environments.
- [x] Database health check probes with automatic connection pool pre-ping.

### Security & Compliance
- [x] Bcrypt password hashing (salt rounds: 12) for all user credentials.
- [x] Server-side JWT signature verification with cryptographic expiration enforcement.
- [x] Secure API key management storing one-way SHA-256 hashes (`hashed_key`), preventing credential leaks.
- [x] Multi-tenant isolation: strict `organization_id` foreign key scoping enforced in all application database queries.
- [x] No committed secrets: configuration driven via environment variables with safe defaults.

### Observability & Monitoring
- [x] Prometheus metrics exposed on `/metrics`: `http_requests_total`, `http_request_latency_seconds`, `recommendations_served_total`, `cold_start_requests_total`.
- [x] Automated drift watchdog tracking feature mean shift and concept drift.
- [x] Gini index monitoring for catalog exposure fairness and recommendation diversity.
- [x] Structured JSON logging with request correlation.

### Model & Data Quality
- [x] Counterfactual offline policy evaluation using Inverse Propensity Scoring (IPS) and Doubly Robust (DR) estimation on logged bandit events.
- [x] Automated retraining triggers when drift threshold is exceeded with a 10-minute cooldown protection.
- [x] Governed MLflow model registry preventing unvalidated model deployments to Production.

---

## 2. Rate Limiting, Backups & Disaster Recovery

### Rate Limiting Strategy
* **Public Recommendation Endpoints (`/v1/recommendations`)**:
  * Default: 120 requests/minute per IP / API key.
  * Burst allowance: 30 requests.
  * Headers: `X-RateLimit-Limit`, `X-RateLimit-Remaining`, `X-RateLimit-Reset`.
* **Behavioral Event Ingestion (`/v1/events`)**:
  * Default: 1,000 requests/minute per store tenant.
  * High-volume batch ingestion: `/v1/events/batch` allows up to 100 events per single payload.

### Database Backups & Recovery
* **PostgreSQL Backup Strategy**:
  * Automated daily physical snapshots (WAL archiving) with point-in-time recovery (PITR) up to 7 days.
  * Logical `pg_dump` daily export of tenant-scoped tables stored in S3/MinIO bucket.
* **Feature Store (Feast) Recovery**:
  * Online store (Redis / SQLite) can be reconstructed from offline event logs via `feast materialize`.
* **Milvus Vector Index Recovery**:
  * Item embeddings are versioned and can be re-indexed from `item_embeddings.npy` or offline MLflow artifact checkpoints within 60 seconds.

---

## 3. Free-Tier Limitations & $0 Cost Deployment

RecommendationOS is engineered so anyone can run the complete system with **$0 mandatory infrastructure costs**:

| Component | $0 Free Tier Choice | Resource Limits | Behavior When Limit Exceeded |
|---|---|---|---|
| **Next.js Frontend** | Vercel Hobby Tier | 100GB bandwidth/month | Throttles to edge static pages |
| **FastAPI Backend** | Render / Railway Free | 512MB RAM, shared vCPU | Sleeps after inactivity (spins up on first ping) |
| **PostgreSQL DB** | Supabase Free / Neon | 500MB storage, 0.5 vCPU | Read-only mode if 500MB exceeded |
| **Feature Store** | Feast with SQLite Online Store | Local disk bound | Zero cost; scales up to ~50k users |
| **Vector DB** | In-Memory NumPy Vector Index | Host RAM bound | Instantaneous retrieval up to 100k items |
| **Kafka Pipeline** | Local In-Memory Streaming Queue | Process memory | Bounded queue, flushes to log |
| **MLflow Registry** | SQLite (`mlflow.db`) + local `mlruns`| Local disk bound | Completely free, full MLflow UI support |

---

## 4. Scaling Architecture: 10x, 100x, and 1,000x Scale

### Current Scale (MVP: ~1,000 QPS, 50k items, 100k users)
* Single-node or dual-container setup.
* Local Redis or in-memory vector cache.
* Single-node Milvus standalone or numpy index.
* SQLite or small cloud PostgreSQL instance.

### 10x Scale (~10,000 QPS, 500k items, 1M users)
* **API Serving**: Deploy FastAPI behind Kubernetes Deployment with HPA (Horizontal Pod Autoscaler) target 65% CPU.
* **Vector Index**: Deploy Milvus Cluster on Kubernetes with dedicated query nodes and standalone index nodes.
* **Caching**: Multi-node Redis Cluster with Sentinel for automatic master failover.
* **Event Stream**: 3-node Apache Kafka cluster with partition key on `organization_id:user_id` to maintain causal event ordering.
* **Feature Store**: Redis-backed Feast online store with asynchronous batch materialization jobs.

### 100x Scale (~100,000 QPS, 5M items, 20M users)
* **Candidate Retrieval**: Multi-level hierarchical indexing (HNSW + IVF_PQ) across partitioned vector shards.
* **Two-Tower Serving**: Run PyTorch User Tower on Triton Inference Server with dynamic batching and TensorRT-LLM acceleration.
* **Feature Processing**: Migrate stream processing from basic Python consumers to Apache Flink streaming stateful pipelines.
* **Database**: PostgreSQL read replicas with PgBouncer connection pooling; separate time-series table partitioning for `user_events`.

### 1,000x Scale (~1,000,000 QPS, 50M items, 200M users)
* **Edge Pre-ranking**: Deploy early-stage candidate filtering at edge locations (Cloudflare Workers / Vercel Edge).
* **Distributed Vector DB**: Global Milvus cluster sharded by product category and geographic region.
* **Feature Store**: Distributed low-latency Key-Value store (Aerospike or ScyllaDB) replacing Redis for sub-millisecond p99 feature retrieval.
* **Model Retraining**: Distributed multi-GPU PyTorch training with Ray Train or Kubeflow Pipelines on partitioned parquet lakehouse data.
