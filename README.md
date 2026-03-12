# RAG IA — Portuguese Opportunities

Système de recherche intelligente sur des offres d'emploi et bourses de recherche portugaises, basé sur un pipeline RAG (Retrieval-Augmented Generation) complet.

## Description

Ce projet permet d'interroger en langage naturel une base de données d'offres d'emploi et de bourses universitaires (principalement de l'Université d'Aveiro). Il combine une recherche sémantique par similarité vectorielle avec la génération de réponses contextualisées via Groq (Llama 3.3).

## Stack technique

| Composant | Technologie |
|---|---|
| Langage | Python 3.12 |
| Pipeline RAG | LangGraph + LangChain |
| Base de données | PostgreSQL + pgvector |
| Embeddings | Gemini Embedding 001 (3072 dims) |
| LLM | Groq — Llama 3.3 70B Versatile |
| API | FastAPI + Uvicorn |
| Gestion des dépendances | uv |

## Architecture

```
SQLite (source)
     │
     ▼
migration.py  ──►  PostgreSQL + pgvector
                        │
                        ▼
indexer.py    ──►  Génération des embeddings (Gemini)
                        │
                        ▼
agent.py      ──►  LangGraph (retrieve → generate)
                        │
                   ┌────┴────┐
                   ▼         ▼
               api.py     main.py
            (FastAPI)     (CLI test)
```

## Structure du projet

```
.
├── src/
│   ├── migration.py   # Migration SQLite → PostgreSQL
│   ├── indexer.py     # Vectorisation des articles avec Gemini
│   ├── agent.py       # Graph LangGraph (RAG)
│   ├── api.py         # API REST FastAPI
│   └── main.py        # Script de test CLI
├── jobs_and_news.db   # Base SQLite source
├── .env               # Variables d'environnement (non versionné)
└── pyproject.toml
```

## Installation

```bash
# Cloner le projet
git clone <repo-url>
cd RAG_IA_Agent_Portuguese_Opportunities

# Installer les dépendances
uv sync
```

## Configuration

Créer un fichier `.env` à la racine :

```env
GEMINI_API_KEY=your_gemini_api_key
GROQ_API_KEY=your_groq_api_key
DATABASE_URL=postgresql://user:password@localhost:5432/dbname
```

## Utilisation

**1. Migrer la base SQLite vers PostgreSQL**
```bash
uv run src/migration.py
```

**2. Vectoriser les articles**
```bash
uv run src/indexer.py
```

**3. Lancer l'API**
```bash
uv run uvicorn src.api:api --reload
```

**4. Tester le pipeline en CLI**
```bash
uv run src/main.py
```

## API Endpoints

| Méthode | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Informations sur l'API |
| `GET` | `/health` | Statut de l'API |
| `POST` | `/query` | Interroge le RAG |
| `GET` | `/items` | Liste tous les articles |
| `GET` | `/items/{id}` | Détail d'un article |

Documentation interactive disponible sur `http://localhost:8000/docs`

### Exemple `/query`

```json
// Request
POST /query
{ "question": "Quelles bourses sont disponibles en informatique ?" }

// Response
{
  "question": "Quelles bourses sont disponibles en informatique ?",
  "answer": "D'après les offres disponibles, l'Université d'Aveiro propose...",
  "sources": ["https://www.ua.pt/pt/noticias/3/95960"]
}
```

## Données

La base contient **62 articles** issus de sources portugaises (Université d'Aveiro), comprenant :
- Offres d'emploi académiques
- Bourses de recherche (BI, BII)
- Appels à candidatures universitaires

Chaque article est indexé avec les champs : `titre`, `description`, `body`, `source`, `date`, `url`.

## Prochaines étapes

- [ ] Ajout de nouvelles sources de données
- [ ] Recherche hybride (sémantique + full-text)
- [ ] Interface web de recherche