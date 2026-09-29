FROM python:3.12-slim AS base

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Copy dependency files
COPY pyproject.toml ./

# Install dependencies
RUN uv sync --no-dev --no-install-project

# Copy application code
COPY src/ src/
COPY alembic.ini ./

# Install the project itself
RUN uv sync --no-dev

EXPOSE 8000

CMD ["uv", "run", "uvicorn", "jevops.main:app", "--host", "0.0.0.0", "--port", "8000"]
