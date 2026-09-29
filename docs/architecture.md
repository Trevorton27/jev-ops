# JevOps Architecture

## Overview

JevOps is an AI Decision Reliability Control Plane that evaluates proposed AI agent actions using TypeSafe AI's Jev model for fast typed semantic judgments, then applies deterministic Python policy rules to return one of four dispositions: **ALLOW**, **RETRY**, **HUMAN_REVIEW**, or **BLOCK**.

## Core Flow

```
Agent proposes action
  → JevOps receives evaluation request
  → Jev model produces semantic judgments (Noul/Choice/Score)
  → Policy engine evaluates rules against judgments
  → Disposition returned to agent
  → If HUMAN_REVIEW: reviewer approves/rejects
  → Outcome recorded for calibration
```

## Key Assumptions

1. **Jev is the semantic layer.** JevOps does not duplicate Jev's judgment capabilities — it wraps them with policy, governance, and calibration.
2. **Policies are deterministic.** Given the same Jev outputs, the same policy always produces the same disposition. No randomness in policy evaluation.
3. **Multi-tenant by default.** Every resource is scoped to an organization. Cross-tenant access is never permitted.
4. **Provider abstraction.** The system supports swappable Jev providers (real TypeSafe, mock, failure simulation) behind a common protocol.
5. **Async-first.** All I/O operations use async patterns. Sync fallbacks exist only for tooling (e.g., Alembic migrations).

## Technology Stack

- **API:** FastAPI + Pydantic v2
- **Database:** PostgreSQL 16 via SQLAlchemy 2.0 (async) + Alembic
- **Cache/Broker:** Redis 7
- **Background Jobs:** Celery
- **Observability:** structlog + OpenTelemetry
- **Frontend:** Next.js 14+ / TypeScript / Tailwind / shadcn/ui
- **Jev Integration:** typesafe-sdk (PyPI)

## Package Structure

- `apps/api` — FastAPI backend (main application)
- `apps/web` — Next.js operations console
- `packages/python-sdk` — Client SDK for integrating with JevOps
