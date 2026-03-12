import sqlite3
import psycopg2
import os


db_url = os.getenv("DATABASE_URL", "postgresql://user:pass@localhost:5432/dbname")

pg_conn = psycopg2.connect(db_url)

sqlite_conn = sqlite3.connect("./jobs_and_news.db")

rows = sqlite_conn.execute(
    "SELECT id, source, title, date, description, body, url FROM items"
).fetchall()

with pg_conn.cursor() as cur:
    print("Activation de pgvector...")
    cur.execute("CREATE EXTENSION IF NOT EXISTS vector;")
    pg_conn.commit() 

    print("Création de la table...")
    cur.execute("""
        CREATE TABLE IF NOT EXISTS items (
            id TEXT PRIMARY KEY,
            source TEXT,
            title TEXT,
            date TEXT,
            description TEXT,
            body TEXT,
            url TEXT,
            embedding vector(768)
        );
    """)
    pg_conn.commit()

with pg_conn.cursor() as cur:
    for row in rows:
        cur.execute("""
            INSERT INTO items (id, source, title, date, description, body, url)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (id) DO NOTHING; -- Évite les erreurs si on relance le script
        """, row)

pg_conn.commit()
print(f"{len(rows)} articles migrés.")