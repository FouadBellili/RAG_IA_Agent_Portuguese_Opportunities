FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

WORKDIR /app

COPY pyproject.toml uv.lock ./

RUN uv pip install --system -r pyproject.toml

COPY . .

ENV PYTHONUNBUFFERED=1

CMD ["python", "src/migration.py"]