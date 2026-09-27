# Production Deployment Guide: RecommendationOS

This guide covers deploying the **RecommendationOS** real-time MLOps platform for **$0 / month** using:
1. **Backend API & ML Serving Engine**: [Railway](https://railway.app) (or [Render](https://render.com)) via Docker.
2. **Frontend Customer Storefront & Admin Cockpit**: [Vercel](https://vercel.com) via Next.js 14.

---

## Architecture Overview

```
                      +-----------------------------------+
                      |         Vercel (Global CDN)        |
                      |        Next.js 14 App Router       |
                      |      http://your-app.vercel.app    |
                      +-----------------+-----------------+
                                        |
                 REST API & WebSockets  | HTTPS Bearer reco_live_...
                                        v
                      +-----------------+-----------------+
                      |     Railway / Render Container     |
                      |      FastAPI Serving Engine        |
                      |   PyTorch Two-Tower Neural Engine  |
                      |    Feast Feature Store + SQLite    |
                      |      MLflow Model Registry         |
                      |    https://your-api.railway.app    |
                      +-----------------------------------+
```

---

## Step 1: Push Code to GitHub

Make sure all your latest changes are pushed to your GitHub repository:

```bash
git add .
git commit -m "feat: complete production-ready recommendation MLOps platform"
git push origin main
```

---

## Step 2: Deploy Backend API on Railway ($0 Starter)

Railway will automatically detect your root [`Dockerfile`](../Dockerfile) and [`railway.json`](../railway.json).

1. Log into [Railway.app](https://railway.app) with your GitHub account.
2. Click **"+ New Project"** &rarr; **"Deploy from GitHub repo"**.
3. Select your repository: `reco-mlops` (or `real-time-recommendation-mlops`).
4. Click **"Deploy Now"**.
5. Go to your service's **"Variables"** tab and add:
   - `PORT` = `8080`
   - `PYTHONUNBUFFERED` = `1`
6. Go to the **"Settings"** tab:
   - Under **Networking**, click **"Generate Domain"** (e.g., `https://reco-mlops-production.up.railway.app`).
7. Test the deployment:
   ```bash
   curl https://your-backend.up.railway.app/health
   # Expected output: {"status":"ok","service":"reco-mlops-serving","model":"TwoTowerRecommender:Production",...}
   ```

*(Alternative: You can use **Render.com** &rarr; **New Web Service** &rarr; Select Docker runtime &rarr; Port 8080).*

---

## Step 3: Deploy Frontend on Vercel ($0 Free Forever)

Vercel provides native edge caching and instant global hosting for the Next.js storefront and dashboard.

1. Log into [Vercel.com](https://vercel.com) with your GitHub account.
2. Click **"Add New..."** &rarr; **"Project"**.
3. Import your GitHub repository.
4. In the configuration screen:
   - **Framework Preset**: Next.js
   - **Root Directory**: Click **Edit** and select **`web`**.
5. Under **Environment Variables**, add:
   - **Key**: `NEXT_PUBLIC_API_URL`
   - **Value**: `https://your-backend.up.railway.app` *(use your Railway domain from Step 2, without a trailing slash)*.
6. Click **"Deploy"**.

Vercel will build and assign you a live HTTPS domain (e.g., `https://reco-mlops.vercel.app`).

---

## Step 4: Verification Checklist

Once both services are deployed, verify the complete loop:

- [ ] **Storefront (`/`)**: Open your Vercel link and switch personas (Alex Chen, Sarah Jenkins, Marcus Vance). Verify product cards update immediately.
- [ ] **Cart & Stream (`/cart`)**: Add an item to cart, click *"Confirm & Trigger MLOps Event"*, and verify in `/history` that the purchase appears as `Materialized`.
- [ ] **Inference Inspector (`/dashboard/recommendations`)**: Verify sub-15ms inference latency and neural match percentages.
- [ ] **A/B Cockpit (`/dashboard/experiments`)**: Verify Pause / Resume toggling on live experiments.
- [ ] **Model Governance (`/dashboard/models`)**: Verify registered MLflow models and Emergency Rollback.
- [ ] **API Keys (`/dashboard/api-keys`)**: Generate a new API key and test it with cURL:
  ```bash
  curl -X GET "https://your-backend.up.railway.app/v1/recommendations?user_id=0&limit=4" \
       -H "Authorization: Bearer <your-generated-key>"
  ```

---

## Step 5: Put Live Links in Your GitHub README

Update your repository's [`README.md`](../README.md) badges with your new live links:

```markdown
[![Live Demo](https://img.shields.io/badge/Live_Demo-Vercel-black?style=for-the-badge&logo=vercel)](https://your-app.vercel.app)
[![API Docs](https://img.shields.io/badge/API_Docs-Swagger-009688?style=for-the-badge&logo=swagger)](https://your-backend.up.railway.app/docs)
[![MLflow](https://img.shields.io/badge/MLflow-Registry-0194E2?style=for-the-badge&logo=mlflow)](https://your-app.vercel.app/dashboard/models)
```
