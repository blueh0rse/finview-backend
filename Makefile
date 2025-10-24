dev:
	PYTHONPATH=. uv run fastapi dev main.py

check:
	uv run ruff check .

lint:
	uv run ruff check . --fix

format:
	uv run ruff format .
