# RAG-backend/dat-ingestion.py

import os
import glob
from qdrant_client import QdrantClient, models
import psycopg2
from embedding_generator import generate_embeddings_for_file # Import from our previous script
from dotenv import load_dotenv

load_dotenv() # Load environment variables from .env file

# --- Configuration ---
QDRANT_HOST = os.getenv("QDRANT_HOST", "localhost")
QDRANT_PORT = int(os.getenv("QDRANT_PORT", "6333"))
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY", None)
QDRANT_COLLECTION_NAME = os.getenv("QDRANT_COLLECTION_NAME", "textbook_embeddings")

NEON_DB_URL = os.getenv("NEON_DB_URL")

TEXTBOOK_DOCS_PATH = "../docs"

def ingest_data():
    print("Starting data ingestion...")

    # 1. Initialize Qdrant Client
    qdrant_client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT, api_key=QDRANT_API_KEY)

    # Ensure collection exists (can be done via qdrant_setup.py or here)
    try:
        qdrant_client.get_collection(collection_name=QDRANT_COLLECTION_NAME)
        print(f"Qdrant collection '{QDRANT_COLLECTION_NAME}' already exists.")
    except Exception:
        print(f"Qdrant collection '{QDRANT_COLLECTION_NAME}' not found. Please run qdrant_setup.py first.")
        return

    # 2. Connect to Neon (Postgres)
    if not NEON_DB_URL:
        print("Error: NEON_DB_URL environment variable not set. Cannot connect to Postgres.")
        return
    conn = None
    try:
        conn = psycopg2.connect(NEON_DB_URL)
        cur = conn.cursor()

        # 3. Process each markdown file
        markdown_files = glob.glob(os.path.join(TEXTBOOK_DOCS_PATH, "*.md"))
        if not markdown_files:
            print(f"No markdown files found in {TEXTBOOK_DOCS_PATH}. Exiting.")
            return

        for file_path in markdown_files:
            print(f"Processing file: {file_path}")
            embeddings_data = generate_embeddings_for_file(file_path)

            points_to_upsert = []
            for entry in embeddings_data:
                # Insert metadata into Neon
                insert_query = """
                INSERT INTO textbook_chunks (chunk_id, chapter_title, section_title, page_url, content)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (chunk_id) DO UPDATE SET
                    chapter_title = EXCLUDED.chapter_title,
                    section_title = EXCLUDED.section_title,
                    page_url = EXCLUDED.page_url,
                    content = EXCLUDED.content;
                """
                # Extract chapter and section from file_path/content if available, otherwise use placeholders
                chapter_title = os.path.basename(file_path).replace('.md', '').replace('-', ' ').title()
                section_title = entry['chunk_id'] # Simple for now, can be improved
                page_url = f"/docs/{os.path.basename(file_path).replace('.md', '')}"

                cur.execute(insert_query, (
                    entry['chunk_id'],
                    chapter_title,
                    section_title,
                    page_url,
                    entry['content']
                ))

                # Prepare points for Qdrant upsert
                points_to_upsert.append(
                    models.PointStruct(
                        id=hash(entry['chunk_id']), # Use hash as ID for Qdrant
                        vector=entry['embedding'],
                        payload={
                            "chunk_id": entry['chunk_id'],
                            "file_path": entry['file_path'],
                            "chapter_title": chapter_title,
                            "page_url": page_url
                        }
                    )
                )

            if points_to_upsert:
                qdrant_client.upsert(
                    collection_name=QDRANT_COLLECTION_NAME,
                    wait=True,
                    points=points_to_upsert
                )
                print(f"Upserted {len(points_to_upsert)} points to Qdrant for {file_path}.")

        conn.commit()
        print("Data ingestion complete.")

    except Exception as e:
        print(f"Error during data ingestion: {e}")
        if conn: conn.rollback()
    finally:
        if conn: cur.close(); conn.close()

if __name__ == "__main__":
    # Ensure .env has QDRANT_HOST, QDRANT_PORT, QDRANT_API_KEY, NEON_DB_URL, EMBEDDING_API_KEY
    ingest_data()
