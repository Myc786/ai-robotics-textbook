# RAG-backend/neon_setup.py

import os
import psycopg2

# --- Configuration ---
NEON_DB_URL = os.getenv("NEON_DB_URL", "postgres://user:password@host:port/database") # Your Neon connection string

def setup_neon_schema():
    print(f"Connecting to Neon Postgres...")
    conn = None
    try:
        conn = psycopg2.connect(NEON_DB_URL)
        cur = conn.cursor()

        # Create tables for storing textbook metadata if they don't exist
        # Example: a table to store chunk_id, chapter_title, section_title, page_url
        create_table_query = """
        CREATE TABLE IF NOT EXISTS textbook_chunks (
            id SERIAL PRIMARY KEY,
            chunk_id VARCHAR(255) UNIQUE NOT NULL,
            chapter_title VARCHAR(255) NOT NULL,
            section_title VARCHAR(255),
            page_url VARCHAR(255) NOT NULL,
            content TEXT NOT NULL
        );
        """
        cur.execute(create_table_query)
        conn.commit()
        print("Neon Postgres schema setup complete: 'textbook_chunks' table ensured.")

    except Exception as e:
        print(f"Error setting up Neon schema: {e}")
    finally:
        if conn:
            cur.close()
            conn.close()

if __name__ == "__main__":
    # Ensure NEON_DB_URL is set as an environment variable
    setup_neon_schema()
