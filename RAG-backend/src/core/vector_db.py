from qdrant_client import AsyncQdrantClient
from qdrant_client.http import models
from typing import List, Optional, Dict, Any
from .config import settings


class VectorDBClient:
    def __init__(self):
        # Initialize the async Qdrant client
        self.client = AsyncQdrantClient(
            url=settings.qdrant_url,
            api_key=settings.qdrant_api_key,
            prefer_grpc=False  # Use HTTP for better compatibility
        )

    async def close(self):
        """Close the Qdrant client connection."""
        await self.client.aclose()

    async def create_collection_if_not_exists(
        self,
        collection_name: str,
        vector_size: int = 1024,  # Default for Cohere multilingual-light-v2.0
        distance: str = "Cosine"
    ):
        """Create a collection if it doesn't exist."""
        try:
            # Check if collection exists
            await self.client.get_collection(collection_name)
        except Exception:
            # Collection doesn't exist, create it
            await self.client.create_collection(
                collection_name=collection_name,
                vectors_config=models.VectorParams(
                    size=vector_size,
                    distance=models.Distance[distance.upper()]
                )
            )

    async def upsert_vectors(
        self,
        collection_name: str,
        points: List[models.PointStruct]
    ):
        """Upsert vectors into the collection."""
        await self.client.upsert(
            collection_name=collection_name,
            points=points
        )

    async def get_collection_info(self, collection_name: str):
        """Get information about a collection."""
        return await self.client.get_collection(collection_name)

    async def search_vectors(
        self,
        collection_name: str,
        query_vector: List[float],
        top_k: int = 5,
        filters: Optional[models.Filter] = None
    ) -> List[models.ScoredPoint]:
        """Search for similar vectors in the collection."""
        results = await self.client.search(
            collection_name=collection_name,
            query_vector=query_vector,
            limit=top_k,
            query_filter=filters,
            with_payload=True
        )
        return results


# Global instance of the vector DB client
vector_db_client = VectorDBClient()