# TechPilot

TechPilot is an AI-powered technical assistant for safe, explainable computer diagnostics. This repository currently implements **Phase 1: a FastAPI backend, SQLite foundation, system diagnostics, and React dashboard**.

## Phase 1 features

- CPU, memory, operating-system, storage, and network diagnostics
- FastAPI endpoints: `/api/health`, `/api/system`, `/api/storage`, `/api/network`
- SQLite database initialization for future diagnostic history
- React + TypeScript + Vite dashboard
- Backend API tests
- No AI provider, command execution, or automatic system modification

## Run locally

### Backend

```bash
cd backend
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

The API is available at `http://localhost:8000`; interactive docs are at `/docs`.

### Frontend

```bash
cd frontend
npm install
npm run dev
```

The dashboard is available at `http://localhost:5173`.

### Tests

```bash
cd backend
pytest
```

## Structure

```text
backend/app/       FastAPI application and diagnostics services
backend/tests/     API and diagnostic tests
frontend/src/      React dashboard
docs/              Architecture and roadmap notes
```

## Safety

TechPilot does not execute commands or modify the host system in Phase 1. Future actions must use an allowlisted registry, explicit permission checks, execution logging, and verification.

## Roadmap

Next: unified diagnostic result schemas and richer system, storage, and network findings. AI troubleshooting and action execution will be added only in later, explicitly planned phases.

Licensed under the MIT License.