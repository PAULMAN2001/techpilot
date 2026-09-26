# TechPilot Architecture

## Phase 1 Overview

Phase 1 keeps the system intentionally small: the FastAPI routes call read-only diagnostic functions, while the React dashboard consumes those endpoints. SQLite is initialized during application startup as a foundation for future history and memory features.

No AI provider or action executor is included yet. Future execution must be isolated behind an allowlist and permission engine.

## Component Diagram

```
React Dashboard (http://localhost:5173)
         ↓
API Calls (GET /api/system, /storage, /network)
         ↓
FastAPI Backend (http://localhost:8000)
         ↓
Diagnostic Functions (psutil, socket, platform)
         ↓
Host Operating System
```

## Key Principles

- **Read-only**: No system modifications in Phase 1
- **Explicit**: No hidden operations or automatic commands
- **Testable**: All API endpoints have unit tests
- **Isolated**: Backend and frontend are loosely coupled via REST
