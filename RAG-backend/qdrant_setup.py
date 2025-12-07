# RAG-backend/qdrant_setup.py

import os
from qdrant_client import QdrantClient, models

# --- Configuration ---
QDRANT_HOST = os.getenv("QDRANT_HOST", "localhost")
QDRANT_PORT = int(os.getenv("QDRANT_PORT", "6333"))
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY", None) # Use if Qdrant is hosted
COLLECTION_NAME = "textbook_embeddings"
VECTOR_SIZE = 1536 # Example for OpenAI ada-002; adjust based on embedding model
DISTANCE_METRIC = models.Distance.COSINE

def setup_qdrant_collection():
    print(f"Connecting to Qdrant at {QDRANT_HOST}:{QDRANT_PORT}...")
    client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT, api_key=QDRANT_API_KEY)

    # Check if collection already exists
    collections = client.get_collections().collections
    existing_collection_names = [c.name for c in collections]

    if COLLECTION_NAME in existing_collection_names:
        print(f"Collection '{COLLECTION_NAME}' already exists. Skipping creation.")
    else:
        print(f"Creating collection '{COLLECTION_NAME}'...")
        client.recreate_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=models.VectorParams(size=VECTOR_SIZE, distance=DISTANCE_METRIC),
        )
        print(f"Collection '{COLLECTION_NAME}' created successfully.")

    print("Qdrant setup complete.")

if __name__ == "__main__":
    # This script assumes Qdrant is already running or accessible.
    # For local development, you might run Qdrant in Docker:
    # docker run -p 6333:6333 -p 6334:6334 qdrant/qdrant
    # For cloud, ensure QDRANT_HOST and QDRANT_API_KEY are set as environment variables.
    setup_qdrant_collection()
