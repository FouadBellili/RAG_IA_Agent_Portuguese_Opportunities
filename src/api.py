import os
import psycopg2
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
from .agent import app as rag_app

load_dotenv()

api = FastAPI(
    title="Portuguese Opportunities RAG",
    description="API de recherche intelligente sur des offres d'emploi et bourses portugaises",
    version="1.0.0"
)

DB_URL = os.getenv("DATABASE_URL")

# --- Schémas Pydantic ---
class QueryRequest(BaseModel):
    question: str

class QueryResponse(BaseModel):
    question: str
    answer: str
    sources: list[str]

# --- Endpoints ---

@api.get("/health")
def health():
    return {"status": "ok"}


@api.post("/query", response_model=QueryResponse)
def query(request: QueryRequest):
    result = rag_app.invoke({
        "question": request.question,
        "context": [],
        "generation": ""
    })
    
    # Les sources sont dans result["context"]
    sources = []
    for doc in result.get("context", []):
        for line in doc.split("\n"):
            if line.startswith("URL:"):
                sources.append(line.replace("URL:", "").strip())
    
    return QueryResponse(
        question=request.question,
        answer=result["generation"],
        sources=sources
    )


@api.get("/items")
def get_items():
    conn = psycopg2.connect(DB_URL)
    with conn.cursor() as cur:
        cur.execute("SELECT id, title, source, url FROM items ORDER BY date DESC")
        rows = cur.fetchall()
    conn.close()
    return [
        {"id": r[0], "title": r[1], "source": r[2], "url": r[3]}
        for r in rows
    ]


@api.get("/items/{item_id}")
def get_item(item_id: int):
    conn = psycopg2.connect(DB_URL)
    with conn.cursor() as cur:
        cur.execute(
            "SELECT id, title, source, date, description, body, url FROM items WHERE id = %s",
            (item_id,)
        )
        row = cur.fetchone()
    conn.close()
    if not row:
        raise HTTPException(status_code=404, detail="Article non trouvé")
    return {
        "id": row[0], "title": row[1], "source": row[2],
        "date": row[3], "description": row[4], "body": row[5], "url": row[6]
    }

@api.get("/")
def root():
    return {"message": "Portuguese Opportunities RAG API", "docs": "/docs"}