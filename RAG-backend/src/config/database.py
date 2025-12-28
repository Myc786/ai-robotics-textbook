import asyncpg
from qdrant_client import QdrantClient
from qdrant_client.http import models
from typing import Optional
from dotenv import load_dotenv
import os

# Load .env file explicitly
load_dotenv()


class QdrantDatabase:
    def __init__(self):
        self.client = QdrantClient(
            url=os.getenv("QDRANT_URL"),
            api_key=os.getenv("QDRANT_API_KEY"),
        )
        self.collection_name = os.getenv("QDRANT_COLLECTION_NAME", "RAG_embeddings")

    def initialize_collection(self):
        """Initialize the Qdrant collection for storing embeddings."""
        # Check if collection already exists
        collections = self.client.get_collections()
        collection_names = [collection.name for collection in collections.collections]

        if self.collection_name not in collection_names:
            # Create collection with appropriate vector configuration
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=models.VectorParams(
                    size=1024,  # Adjust based on embedding model (e.g., Cohere's embedding size)
                    distance=models.Distance.COSINE
                )
            )
            print(f"Created Qdrant collection: {self.collection_name}")
        else:
            print(f"Qdrant collection {self.collection_name} already exists")

    def get_client(self):
        return self.client


class PostgresDatabase:
    def __init__(self):
        self.database_url = os.getenv("DATABASE_URL")
        self.connection = None

    async def connect(self):
        """Establish connection to Neon Postgres database."""
        try:
            self.connection = await asyncpg.connect(dsn=self.database_url)
            print("Connected to Neon Postgres database")
        except Exception as e:
            print(f"Error connecting to Neon Postgres: {e}")
            raise

    async def disconnect(self):
        """Close connection to Neon Postgres database."""
        if self.connection:
            await self.connection.close()

    async def initialize_schema(self):
        """Initialize the database schema."""
        if not self.connection:
            await self.connect()

        # Create tables for Book, Chapter, Section, Chunk, Query, Response
        queries = [
            """
            CREATE TABLE IF NOT EXISTS books (
                book_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                title VARCHAR(500) NOT NULL,
                author VARCHAR(200),
                isbn VARCHAR(20),
                metadata JSONB,
                created_at TIMESTAMP DEFAULT NOW(),
                updated_at TIMESTAMP DEFAULT NOW()
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS chapters (
                chapter_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                book_id UUID REFERENCES books(book_id),
                title VARCHAR(300) NOT NULL,
                chapter_number INTEGER,
                content TEXT,
                created_at TIMESTAMP DEFAULT NOW(),
                updated_at TIMESTAMP DEFAULT NOW()
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS sections (
                section_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                chapter_id UUID REFERENCES chapters(chapter_id),
                title VARCHAR(300) NOT NULL,
                section_number INTEGER,
                content TEXT,
                created_at TIMESTAMP DEFAULT NOW(),
                updated_at TIMESTAMP DEFAULT NOW()
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS chunks (
                chunk_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                book_id UUID REFERENCES books(book_id),
                chapter_id UUID REFERENCES chapters(chapter_id),
                section_id UUID REFERENCES sections(section_id),
                content TEXT NOT NULL,
                token_count INTEGER,
                vector_id VARCHAR(100),  -- ID in Qdrant
                created_at TIMESTAMP DEFAULT NOW(),
                updated_at TIMESTAMP DEFAULT NOW()
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS queries (
                query_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                query_text TEXT NOT NULL,
                mode VARCHAR(20) CHECK (mode IN ('global', 'selected_text')),
                selected_text TEXT,
                created_at TIMESTAMP DEFAULT NOW()
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS responses (
                response_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                query_id UUID REFERENCES queries(query_id),
                response_text TEXT NOT NULL,
                confidence_score DECIMAL(3, 2),
                retrieved_chunks JSONB,
                execution_time_ms INTEGER,
                created_at TIMESTAMP DEFAULT NOW()
            );
            """
        ]

        for query in queries:
            await self.connection.execute(query)

        print("Neon Postgres schema initialized")


# Global instances
qdrant_db = QdrantDatabase()
postgres_db = PostgresDatabase()