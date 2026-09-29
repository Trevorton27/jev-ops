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
