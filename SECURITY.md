# Security Policy & Threat Model

RecommendationOS is designed with defense-in-depth security principles across authentication, authorization, multi-tenant isolation, and data protection.

---

## 1. Threat Model & Security Controls

| Threat Vector | Mitigation Strategy & Implementation Controls |
|---|---|
| **Cross-Tenant Data Exfiltration** | All relational models include indexed `organization_id` foreign keys. Application endpoints extract and enforce tenant identity from cryptographically signed JWT claims or validated API keys. |
| **API Key Compromise** | Secret API keys (`reco_live_...`) are generated with 192 bits of cryptographic entropy (`secrets.token_hex(24)`). Plaintext keys are never stored; only one-way SHA-256 hashes are persisted in the database. |
| **Credential & Password Cracking** | User passwords are salted and hashed using `bcrypt` (12 rounds) with length sanitation to prevent buffer issues. Plaintext passwords never touch logs or databases. |
| **SQL Injection (SQLi)** | All database queries are executed via SQLAlchemy 2.0 ORM with parameterized query bindings. Raw string concatenation in SQL queries is strictly prohibited. |
| **Denial of Service (DoS) on Serving** | Recommendation pipeline features hard timeout limits (0.5s) and 4-tier fallback degradation. Requests exceeding compute budgets degrade gracefully to cached or popular candidates. |
| **Man-in-the-Middle (MitM) Attacks** | All production network endpoints require TLS 1.3 encryption. JWT tokens use `HS256` (or `RS256` in production clusters) with explicit signature verification. |
| **Data Drift & Poisoning** | Automated drift watchdog tracks incoming feature statistics and counterfactual distributions. Retraining runs require passing offline evaluation gates before production registry promotion. |

---

## 2. API Key Security & Lifecycle

1. **Creation**:
   * API keys are formatted as `reco_live_<random_hex>`.
   * A 12-character prefix (e.g. `reco_live_a1b2`) is retained for administrative recognition.
2. **Storage**:
   * The database persists `hashed_key = SHA-256(secret_key)`.
   * Stored hashes are unique-indexed for $O(1)$ lookups.
3. **Revocation**:
   * Administrators can instantly revoke keys via `DELETE /v1/api-keys/{id}`, terminating access across all worker nodes.

---

## 3. Reporting Security Vulnerabilities

If you discover a security vulnerability in this repository, please do not open a public issue. Email the repository maintainers or submit an encrypted report via GitHub Private Vulnerability Reporting.
