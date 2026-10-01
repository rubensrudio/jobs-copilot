# Jobs Copilot

## Overview
Jobs Copilot is a job-search copilot. Paste a job posting URL (or its text) and get a
fit score (0–100) with requirement-level evidence, the gaps against your profile, and
a tailored CV exported as PDF. Your profile is built from an uploaded CV (PDF) and can
be edited manually. Later phases add daily automatic collection from public job feeds,
a ranking model learned from your "apply"/"skip" decisions, and highlights for new
relevant postings.

Multi-user, invite-only, login with Google or GitHub.

## Architecture
Monorepo:

- `backend/` — FastAPI (Python 3.12, uv). Analysis runs as a LangGraph `StateGraph`
  (`fetch → extract → retrieve → match → score`). The score is computed by plain code
  (must-have weight 3, nice-to-have weight 1); the LLM only classifies requirements and
  quotes evidence. MongoDB (+ GridFS for PDFs) stores raw postings and user data;
  Pinecone stores embeddings (one namespace per user); XGBoost + scikit-learn ranking
  models are tracked and registered in MLflow (one model per user).
- `frontend/` — Angular standalone SPA (signals, no UI library).
- `infra/` — AWS SAM: EventBridge daily cron → Lambda `collector_trigger` → backend
  internal collection endpoint (token read from Secrets Manager).

## Prerequisites
- Docker (with Docker Compose v2)
- [uv](https://docs.astral.sh/uv/) (Python 3.12)
- Node.js 24 + npm
- AWS SAM CLI (only for the `infra/` deployment)
- Accounts/keys: OpenAI, Pinecone, Google and GitHub OAuth apps

## Local setup
```bash
cp .env.example .env          # fill in the values; never commit .env
docker compose up -d          # MongoDB on :27017, MLflow UI on http://localhost:5001
```

Backend:
```bash
cd backend
uv sync
uv run uvicorn app.main:app --reload
```

Frontend:
```bash
cd frontend
npm ci
npx ng serve                  # http://localhost:4200 (proxies /api to the backend)
```

Pinecone: create the index named by `PINECONE_INDEX` once in the Pinecone console.

## Security notes
- Never commit `.env` or any real key/secret; only `.env.example` (names only) is versioned.
- `SESSION_SECRET` and `COLLECTOR_TOKEN` must be at least 32 random bytes.
- Personal contact data from the uploaded CV is never sent to external providers after extraction.