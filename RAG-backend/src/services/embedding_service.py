import cohere
from typing import List, Optional
import logging
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from src.core.config import settings
from src.core.logger import setup_logger


class EmbeddingService:
    def __init__(self):
        self.client = cohere.AsyncClient(api_key=settings.cohere_api_key)
        self.model = settings.embedding_model
        self.logger = setup_logger(__name__)

    async def embed_texts(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for a list of texts using Cohere.

        Args:
            texts: List of texts to embed

        Returns:
            List of embeddings (each embedding is a list of floats)
        """
        try:
            self.logger.info(f"Generating embeddings for {len(texts)} texts using model: {self.model}")

            response = await self.client.embed(
                texts=texts,
                model=self.model,
                input_type="search_document"  # Optimize for document search
            )

            embeddings = [embedding for embedding in response.embeddings]
            self.logger.info(f"Successfully generated {len(embeddings)} embeddings")

            return embeddings

        except Exception as e:
            self.logger.error(f"Error generating embeddings: {str(e)}")
            raise

    async def embed_query(self, query: str) -> List[float]:
        """
        Generate embedding for a single query using Cohere.

        Args:
            query: The query text to embed

        Returns:
            Embedding as a list of floats
        """
        try:
            self.logger.info(f"Generating embedding for query using model: {self.model}")

            response = await self.client.embed(
                texts=[query],
                model=self.model,
                input_type="search_query"  # Optimize for search queries
            )

            embedding = response.embeddings[0]
            self.logger.info("Successfully generated query embedding")

            return embedding

        except Exception as e:
            self.logger.error(f"Error generating query embedding: {str(e)}")
            raise

    async def close(self):
        """Close the Cohere client connection."""
        if hasattr(self.client, 'close'):
            await self.client.close()


# Global instance of the embedding service
embedding_service = EmbeddingService()