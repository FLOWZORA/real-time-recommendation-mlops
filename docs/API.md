# RecommendationOS — API Reference

RecommendationOS exposes a clean, high-performance RESTful API adhering to OpenAPI 3.1 specifications.

- **Interactive Swagger UI**: `http://localhost:8080/docs`
- **ReDoc Documentation**: `http://localhost:8080/redoc`
- **Default Base URL**: `http://localhost:8080`

---

## 1. Authentication & Security

All requests to protected endpoints require authentication via:
1. **Bearer JWT Token**: `Authorization: Bearer <access_token>`
2. **Organization API Key**: `Authorization: Bearer reco_live_<secret_key>`

### Roles & RBAC:
* `CUSTOMER`: Access profile, trigger behavioral events, request personalized recommendations.
* `STORE_ADMIN`: Manage store products, generate/revoke API keys, inspect analytics, view events.
* `ML_ENGINEER`: Deploy/rollback models in the MLflow registry, configure A/B tests, trigger retrain runs.

---

## 2. Authentication Endpoints (`/v1/auth`)

### `POST /v1/auth/signup`
Create a new store administrator account and organization.

**Request:**
```json
{
  "email": "owner@brandstore.com",
  "password": "StrongPassword123!",
  "full_name": "Store Owner",
  "organization_name": "BrandStore Audio",
  "role": "STORE_ADMIN"
}
```

**Response (200 OK):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsIn...",
  "token_type": "bearer",
  "user_id": "78bfae34-1290-48e2-b34e-89a1c92bc491",
  "email": "owner@brandstore.com",
  "role": "STORE_ADMIN",
  "organization_id": "1894a821-34df-419b-a7e1-889adce7124f"
}
```

### `POST /v1/auth/login`
Authenticate existing users.

---

## 3. Product Catalog Endpoints (`/v1/products`)

### `GET /v1/products`
List catalog products with pagination, category filtering, and search.

**Query Parameters:**
* `category_name` (optional): Filter by category (e.g. `Audio & Sound`)
* `search` (optional): Keyword search on product title
* `skip` (default: 0): Pagination offset
* `limit` (default: 50, max: 100): Page size

### `GET /v1/products/{product_id}`
Retrieve a single product by UUID or numeric catalog ID (0..499).

---

## 4. Behavioral Events Ingestion (`/v1/events`)

RecommendationOS ingests real-time events, stores them in PostgreSQL, streams them to Kafka, and updates Feast online user feature vectors.

### `POST /v1/events`
**Request:**
```json
{
  "user_id": "user_42",
  "item_id": 18,
  "event_type": "product_click",
  "propensity": 0.1,
  "metadata": {
    "source_surface": "home_carousel",
    "dwell_time_seconds": 12.4
  }
}
```

**Supported Event Types & Implicit Rewards:**
| Event Type | Implicit Reward | Description |
|---|---|---|
| `product_view` | `0.1` | User viewed product card or detail page |
| `product_click` | `0.5` | User clicked product card for details |
| `add_to_cart` | `0.5` | User added product to cart |
| `purchase` | `1.0` | User completed purchase (triggers online SGD) |

---

## 5. Recommendation Serving (`/v1/recommendations`)

### `GET /v1/recommendations`
Retrieve personalized recommendations for a user.

**Query Parameters:**
* `user_id` (required): User ID string or numeric index (e.g. `0` or `user_123`)
* `limit` (default: 10, max: 50): Number of items to return
* `disable_cache` (default: false): Bypass Redis cache for testing

**Response (200 OK):**
```json
{
  "user_id": "0",
  "organization_id": "demo-store",
  "cold_start": false,
  "strategy": "two_tower_milvus",
  "model_version": "TwoTowerRecommender:Production",
  "latency_ms": 3.84,
  "cache_hit": false,
  "recommendations": [12, 18, 5, 2, 42, 9, 14, 21, 33, 7],
  "detailed_recommendations": [
    {
      "item_id": 12,
      "title": "Sony WH-1000XM5 Wireless Headphones",
      "category": "Audio & Sound",
      "price": 398.00,
      "rating": 4.8,
      "score": 0.92,
      "rank": 1,
      "source": "two_tower_retrieval",
      "reason": "Matches user profile in Audio & Sound"
    }
  ],
  "user_features": {
    "total_views": 18,
    "total_clicks": 6,
    "total_purchases": 2
  },
  "explanation": "Personalized for Alex Chen: Audio & Hi-Fi Gear"
}
```

### `GET /v1/similar/{product_id}`
Retrieve nearest neighbor products using Item Tower embeddings and vector ANN search.

---

## 6. A/B Testing (`/v1/experiments`)

### `GET /v1/experiments`
List active experiments with sample sizes, variant CTRs, and two-proportion Z-test statistical significance.

---

## 7. Model Governance (`/v1/models`)

### `POST /v1/models/deploy`
Promote a registered model version to `Staging`, `Canary`, or `Production`.
```json
{
  "model_name": "TwoTowerRecommender",
  "version": "2",
  "target_stage": "Production"
}
```

### `POST /v1/models/rollback`
Roll back to previous stable production checkpoint.

---

## 8. API Key Management (`/v1/api-keys`)

### `POST /v1/api-keys`
Generate an API key (`reco_live_...`).
```json
{
  "name": "Production Storefront Key",
  "scopes": ["read:recommendations", "write:events", "read:products"]
}
```
*Note: The plaintext secret key is only returned in the response of this POST request and stored as a one-way SHA-256 hash in the database.*
