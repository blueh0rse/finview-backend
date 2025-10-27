run:
	docker compose up --build

api:
	uv run fastapi dev api/main.py

check:
	uv run ruff check .

lint:
	uv run ruff check . --fix

format:
	uv run ruff format .

clean:
	docker compose down
