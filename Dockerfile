FROM python:3.12-slim

WORKDIR /app

RUN python -m ensurepip && python -m pip install --upgrade pip uv

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-cache

COPY . .

EXPOSE 8000

CMD ["sh", "-c", "uv run alembic upgrade head && uv run fastapi dev api/main.py --host 0.0.0.0 --port 8000"]
