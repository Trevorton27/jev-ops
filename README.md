# JevOps

AI Decision Reliability Control Plane.

Evaluates proposed AI agent actions using TypeSafe AI's Jev model for fast typed semantic judgments, then applies deterministic Python policy rules to return one of four dispositions: **ALLOW**, **RETRY**, **HUMAN_REVIEW**, or **BLOCK**.

## Quick Start

```bash
# Start infrastructure
make up

# Install dependencies
make install

# Run migrations
make migrate

# Start API server
make dev
```

## Development

```bash
make lint      # Check code style
make format    # Auto-format code
make test      # Run tests
```

## Architecture

```
                         ┌──────────────────────┐
                         │       Vercel          │
                         │   Next.js Web Console │
                         │   (Operations UI)     │
                         └──────────┬────────────┘
                                    │
                          NEXT_PUBLIC_API_URL
                            (HTTPS requests)
                                    │
                                    ▼
┌───────────────────────────────────────────────────────┐
│                      Railway                          │
│                                                       │
│   ┌───────────────────┐      ┌──────────────────┐    │
│   │   API Service      │      │  Worker Service   │    │
│   │   (FastAPI)        │      │  (Celery)         │    │
│   │                    │      │                   │    │
│   │ - Decision engine  │      │ - Async tasks     │    │
│   │ - Policy eval      │ ───▶ │ - Drift detection │    │
│   │ - REST API         │ task │ - Replay runs     │    │
│   │ - Alembic migrate  │ queue│                   │    │
│   └────────┬───────────┘      └─────────┬─────────┘    │
│            │                            │              │
└────────────┼────────────────────────────┼──────────────┘
             │                            │
        ┌────┴────┐                 ┌─────┴─────┐
        │  Neon   │                 │  Upstash  │
        │Postgres │                 │   Redis   │
        │         │                 │           │
        │ - Orgs  │                 │ - Celery  │
        │ - Agents│                 │   broker  │
        │ - Deci- │                 │ - Result  │
        │   sions │                 │   backend │
        │ - Poli- │                 │ - Rate    │
        │   cies  │                 │   limits  │
        └─────────┘                 └───────────┘

                    ┌───────────────┐
                    │  AI Agent     │
                    │  (Your App)   │
                    └───────┬───────┘
                            │
                   POST /v1/decisions
                   X-API-Key header
                            │
                            ▼
                    ┌───────────────┐
                    │  JevOps API   │
                    │  (Railway)    │
                    └───────────────┘
                            │
                    Evaluate action via
                    Jev model + policies
                            │
                            ▼
                 ┌─────────────────────┐
                 │  ALLOW | RETRY |    │
                 │  HUMAN_REVIEW |     │
                 │  BLOCK              │
                 └─────────────────────┘
```

**Request flow:** An AI agent sends a proposed action to the JevOps API on Railway. The API evaluates it using the Jev model (TypeSafe AI) for semantic judgment, then applies deterministic policy rules, and returns a disposition. The Celery worker on Railway handles async tasks like drift detection and replay runs, using Upstash Redis as the message broker. The Next.js console on Vercel provides a UI for reviewing decisions, managing policies, and monitoring agents.

## Project Structure

```
jevops/
├── apps/api/          # FastAPI backend
├── apps/web/          # Next.js operations console
├── packages/python-sdk/  # Python client SDK
├── docs/              # Documentation
├── policies/examples/ # Example policy definitions
└── docker-compose.yml # PostgreSQL + Redis
```
