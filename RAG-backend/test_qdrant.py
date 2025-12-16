import asyncio
import os
from qdrant_client import AsyncQdrantClient
from src.core.config import settings

async def test_qdrant_connection():
    print("Testing Qdrant connection...")
    print(f"Qdrant URL: {settings.qdrant_url}")
    print(f"Environment: {settings.environment}")

    try:
        client = AsyncQdrantClient(
            url=settings.qdrant_url,
            api_key=settings.qdrant_api_key,
            prefer_grpc=False
        )

        print("Attempting to connect to Qdrant...")
        collections = await client.get_collections()
        print(f"Connected successfully! Available collections: {collections}")

        # Try to get or create the document_chunks collection
        collection_name = "document_chunks"
        try:
            collection_info = await client.get_collection(collection_name)
            print(f"Collection '{collection_name}' exists: {collection_info}")
        except Exception as e:
            print(f"Collection '{collection_name}' doesn't exist, would be created on first use: {e}")

        await client.aclose()
        print("Connection test completed successfully!")
        return True

    except Exception as e:
        print(f"Error connecting to Qdrant: {str(e)}")
        return False

if __name__ == "__main__":
    asyncio.run(test_qdrant_connection())