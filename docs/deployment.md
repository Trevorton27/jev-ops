# Deployment

## Development

```bash
make up        # Start Postgres + Redis
make install   # Install Python dependencies
make migrate   # Run database migrations
make dev       # Start API server with hot reload
```

## Docker Compose (Production)

```bash
docker compose --profile production up -d
```

This starts: PostgreSQL, Redis, API server, Web console, Celery worker.

## Environment Variables

See `.env.example` for all configuration options. Key variables:

- `JEVOPS_DB_*`: Database connection
- `JEVOPS_REDIS_*`: Redis connection
- `JEVOPS_JEV_PROVIDER`: `mock`, `typesafe`, or `failure`
- `JEVOPS_SECURITY_API_KEY_PEPPER`: Secret pepper for API key hashing
- `JEVOPS_OTEL_ENABLED`: Enable OpenTelemetry tracing

## Health Checks

- `GET /health` — Root health check
- `GET /v1/health` — API version health check
