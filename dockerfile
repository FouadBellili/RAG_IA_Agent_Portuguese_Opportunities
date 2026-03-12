FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

WORKDIR /app

# On copie les fichiers de config
COPY pyproject.toml uv.lock ./

# On installe les dépendances SANS créer de venv (plus simple pour Docker)
RUN uv pip install --system -r pyproject.toml

# On copie le reste du code
COPY . .

# On s'assure que les logs s'affichent
ENV PYTHONUNBUFFERED=1

CMD ["python", "src/migration.py"]