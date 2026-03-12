import os
import psycopg2
from typing import List, TypedDict
from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langgraph.graph import StateGraph, START, END

load_dotenv()

EMBEDDING_MODEL = "models/gemini-embedding-001"
LLM_MODEL = "gemini-2.0-flash-lite"

class GraphState(TypedDict):
    question: str
    context: List[str]
    generation: str

embeddings = GoogleGenerativeAIEmbeddings(model=EMBEDDING_MODEL,
    task_type="retrieval_document",
    output_dimensionality=768)
llm = ChatGoogleGenerativeAI(model=LLM_MODEL, temperature=0,google_api_key=os.getenv("GEMINI_API_KEY"))

DB_URL = os.getenv("DATABASE_URL")

def retrieve(state: GraphState):
    print("--- RECHERCHE SEMANTIQUE (SQL) ---")
    question = state["question"]
    
    query_vector = embeddings.embed_query(question)
    
    conn = psycopg2.connect(DB_URL)
    with conn.cursor() as cur:
        cur.execute("""
            SELECT description, title, url 
            FROM items 
            ORDER BY embedding <=> %s::vector 
            LIMIT 3
        """, (query_vector,))
        rows = cur.fetchall()
    conn.close()

    context = [f"Titre: {r[1]}\nDescription: {r[0]}\nURL: {r[2]}" for r in rows if r[0]]
    print(f"Documents trouvés : {len(context)}")
    return {"context": context}

def generate(state: GraphState):
    print("--- GENERATION GEMINI ---")
    question = state["question"]
    context = "\n\n---\n\n".join(state["context"])
    
    if not state["context"]:
        return {"generation": "Je n'ai trouvé aucune offre correspondante dans la base."}

    prompt = f"""Tu es un assistant expert pour les opportunités professionnelles au Portugal.
    Réponds en français à la question en utilisant UNIQUEMENT le contexte fourni.
    
    CONTEXTE:
    {context}
    
    QUESTION:
    {question}
    """
    
    response = llm.invoke(prompt)
    return {"generation": response.content}

# 5. Construction du Graphe
workflow = StateGraph(GraphState)
workflow.add_node("retrieve", retrieve)
workflow.add_node("generate", generate)
workflow.add_edge(START, "retrieve")
workflow.add_edge("retrieve", "generate")
workflow.add_edge("generate", END)

app = workflow.compile()