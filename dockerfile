FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

WORKDIR /app

COPY pyproject.toml uv.lock ./

RUN uv sync --frozen

COPY . .

ENV PYTHONUNBUFFERED=1

CMD ["uv", "run", "uvicorn", "src.api:api", "--host", "0.0.0.0", "--port", "8000"]