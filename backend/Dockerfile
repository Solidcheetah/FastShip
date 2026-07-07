FROM python:3.14-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

WORKDIR /app

COPY pyproject.toml uv.lock ./

RUN uv sync --locked --no-cache

COPY . .

ENTRYPOINT ["uv", "run", "fastapi", "run", "app/main.py", "--port", "8000"]


