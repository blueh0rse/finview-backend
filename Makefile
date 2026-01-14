.PHONY: api check lint format clean db stop run test test-db-up test-db-down

run:
	docker compose up

stop:
	docker compose down

api:
	uv run fastapi dev src/api/main.py

check:
	uv run ruff check .

lint:
	uv run ruff check . --fix

format:
	uv run ruff format .

clean:
	docker compose down -v

db:
	docker compose up db adminer

dbmigrate:
	uv run alembic revision --autogenerate -m "update schema"

dbupgrade:
	uv run alembic upgrade head


test: test-db-up
	@PYTHONPATH=. DATABASE_URL=postgresql+psycopg2://test:test@localhost:5433/finview_test DB_URL=postgresql+psycopg2://test:test@localhost:5433/finview_test $(shell [ -x .venv/bin/python ] && echo .venv/bin/python || echo python) -m pytest -x; EXIT_CODE=$$?; $(MAKE) test-db-down; exit $$EXIT_CODE

test-db-up:
	@docker compose -f docker-compose.test.yaml up -d
	@echo "Waiting for test database..."
	@until docker inspect --format='{{.State.Health.Status}}' finview-db-test | grep healthy; do sleep 1; done

test-db-down:
	@docker compose -f docker-compose.test.yaml down -v