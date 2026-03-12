# RAG IA — Portuguese Opportunities

Système de recherche intelligente sur des offres d'emploi et bourses de recherche portugaises, basé sur un pipeline RAG (Retrieval-Augmented Generation) complet.

## Description

Ce projet permet d'interroger en langage naturel une base de données d'offres d'emploi et de bourses universitaires (principalement de l'Université d'Aveiro). Il combine une recherche sémantique par similarité vectorielle avec la génération de réponses contextualisées via l'API Gemini.

## Stack technique

| Composant | Technologie |
|---|---|
| Langage | Python 3.12 |
| Pipeline RAG | LangGraph + LangChain |
| Base de données | PostgreSQL + pgvector |
| Embeddings | Gemini Embedding 001 (3072 dims -> 768 dims) |
| LLM | Gemini 2.0 Flash |
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
                        ▼
main.py       ──►  Script de test du pipeline
```

## Structure du projet

```
.
├── src/
│   ├── migration.py   # Migration SQLite → PostgreSQL
│   ├── indexer.py     # Vectorisation des articles avec Gemini
│   ├── agent.py       # Graph LangGraph (RAG)
│   └── main.py        # Script de test du pipeline
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

**3. Tester le pipeline RAG**
```bash
uv run src/main.py
```

## Exemple de résultat

```
============================================================
QUESTION : Quelles sont les bourses disponibles à l'Université d'Aveiro ?
============================================================
--- RECHERCHE SEMANTIQUE (SQL) ---
Documents trouvés : 3
--- GENERATION GEMINI ---

--- RÉPONSE ---
D'après les offres disponibles, l'Université d'Aveiro propose
des Bolsas de Investigação (BI) et des Bolsas de Iniciação à
Investigação (BII) dans des domaines comme l'ingénierie
informatique, la physique et les matériaux...
```

## Données

La base contient **62 articles** issus de sources portugaises (Université d'Aveiro), comprenant :
- Offres d'emploi académiques
- Bourses de recherche (BI, BII)
- Appels à candidatures universitaires

Chaque article est indexé avec les champs : `titre`, `description`, `body`, `source`, `date`, `url`.

## Prochaines étapes

- [ ] Exposition via API REST (FastAPI)
- [ ] Interface web de recherche
- [ ] Ajout de nouvelles sources de données
- [ ] Recherche hybride (sémantique + full-text)
