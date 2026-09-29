.PHONY: dev test lint format migrate up down install

install:
	cd apps/api && uv sync --all-extras

dev:
	cd apps/api && uv run uvicorn jevops.main:app --reload --host 0.0.0.0 --port 8000

test:
	cd apps/api && uv run pytest -xvs

lint:
	cd apps/api && uv run ruff check src/ tests/
	cd apps/api && uv run ruff format --check src/ tests/

format:
	cd apps/api && uv run ruff check --fix src/ tests/
	cd apps/api && uv run ruff format src/ tests/

migrate:
	cd apps/api && uv run alembic upgrade head

up:
	docker compose up -d

down:
	docker compose down
