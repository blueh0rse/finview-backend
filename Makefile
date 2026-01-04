.PHONY: api check lint format clean db stop run

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
