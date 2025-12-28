import cohere
from typing import List, Dict, Any
from src.config.settings import settings
from src.config.database import qdrant_db, postgres_db
from qdrant_client.http import models
import uuid


class RetrievalService:
    def __init__(self):
        self.cohere_client = cohere.Client(api_key=settings.cohere_api_key)
        self.qdrant_client = qdrant_db.get_client()
        self.qdrant_collection = qdrant_db.collection_name
        self.postgres_db = postgres_db
        self.top_k = settings.top_k
        self.similarity_threshold = settings.similarity_threshold

    async def retrieve_relevant_chunks(self, query: str, top_k: int = None, threshold: float = None) -> List[Dict[str, Any]]:
        """
        Retrieve the most relevant chunks for a given query.
        
        Args:
            query: The query string
            top_k: Number of top results to retrieve (defaults to settings)
            threshold: Minimum similarity threshold (defaults to settings)
            
        Returns:
            List of relevant chunks with metadata
        """
        if top_k is None:
            top_k = self.top_k
        if threshold is None:
            threshold = self.similarity_threshold
            
        # Generate embedding for the query
        # embed-english-v3.0 requires input_type parameter
        query_embedding = self.cohere_client.embed(
            texts=[query],
            model="embed-english-v3.0",
            input_type="search_query"
        ).embeddings[0]
        
        # Search in Qdrant
        search_result = self.qdrant_client.search(
            collection_name=self.qdrant_collection,
            query_vector=query_embedding,
            limit=top_k,
            score_threshold=threshold
        )
        
        # Format results
        retrieved_chunks = []
        for result in search_result:
            chunk_data = {
                "chunk_id": result.payload.get("chunk_id", ""),
                "book_id": result.payload.get("book_id", ""),
                "chapter_id": result.payload.get("chapter_id", ""),
                "section_id": result.payload.get("section_id", ""),
                "content": result.payload.get("content", ""),
                "similarity_score": result.score
            }
            retrieved_chunks.append(chunk_data)
        
        return retrieved_chunks

    async def retrieve_by_chunk_ids(self, chunk_ids: List[str]) -> List[Dict[str, Any]]:
        """
        Retrieve specific chunks by their IDs.
        
        Args:
            chunk_ids: List of chunk IDs to retrieve
            
        Returns:
            List of chunks with metadata
        """
        # Convert string IDs to UUIDs if needed and retrieve from Qdrant
        points = self.qdrant_client.retrieve(
            collection_name=self.qdrant_collection,
            ids=chunk_ids,
            with_payload=True,
            with_vectors=False
        )
        
        retrieved_chunks = []
        for point in points:
            chunk_data = {
                "chunk_id": point.payload.get("chunk_id", ""),
                "book_id": point.payload.get("book_id", ""),
                "chapter_id": point.payload.get("chapter_id", ""),
                "section_id": point.payload.get("section_id", ""),
                "content": point.payload.get("content", ""),
                "similarity_score": 1.0  # Exact match
            }
            retrieved_chunks.append(chunk_data)
        
        return retrieved_chunks

    async def validate_retrieval_quality(self, query: str, retrieved_chunks: List[Dict[str, Any]]) -> bool:
        """
        Validate if the retrieved chunks are relevant to the query.
        
        Args:
            query: The original query
            retrieved_chunks: List of retrieved chunks
            
        Returns:
            True if retrieval quality is acceptable, False otherwise
        """
        # Simple validation: check if any chunks have similarity above threshold
        if not retrieved_chunks:
            return False
            
        # Check if at least one chunk has acceptable similarity
        for chunk in retrieved_chunks:
            if chunk.get("similarity_score", 0) >= self.similarity_threshold:
                return True
                
        return False