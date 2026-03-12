import os
from dotenv import load_dotenv
import psycopg2
from langchain_google_genai import GoogleGenerativeAIEmbeddings

load_dotenv()


def index_data():
    embeddings_model = GoogleGenerativeAIEmbeddings(
    model="models/gemini-embedding-001",
    task_type="retrieval_document",
    output_dimensionality=768
    )
    conn = psycopg2.connect(os.getenv("DATABASE_URL"))
    cur = conn.cursor()

    cur.execute("SELECT id, description FROM items WHERE embedding IS NULL")
    rows = cur.fetchall()
    
    print(f"Extraction de {len(rows)} articles à vectoriser...")

    for item_id, description in rows:
        if not description: continue
        
        vector = embeddings_model.embed_query(description)
        
        cur.execute(
            "UPDATE items SET embedding = %s WHERE id = %s",
            (vector, item_id)
        )
        print(f" Article {item_id} indexé.")

    conn.commit()
    cur.close()
    conn.close()
    print("Indexation terminée !")

if __name__ == "__main__":
    index_data()