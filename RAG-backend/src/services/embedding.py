import cohere
from typing import List, Dict, Any
from src.config.settings import settings
from src.config.database import qdrant_db, postgres_db
import uuid
from qdrant_client.http import models


class EmbeddingService:
    def __init__(self):
        self.cohere_client = cohere.Client(api_key=settings.cohere_api_key)
        self.qdrant_client = qdrant_db.get_client()
        self.qdrant_collection = qdrant_db.collection_name
        self.postgres_db = postgres_db

    def generate_embeddings(self, texts: List[str], model: str = "embed-english-v3.0", is_query: bool = False) -> List[List[float]]:
        """
        Generate embeddings for a list of texts using Cohere.

        Args:
            texts: List of text strings to embed
            model: Cohere embedding model to use
            is_query: If True, use search_query input type, else search_document

        Returns:
            List of embedding vectors
        """
        # embed-english-v3.0 requires input_type parameter
        input_type = "search_query" if is_query else "search_document"
        response = self.cohere_client.embed(
            texts=texts,
            model=model,
            input_type=input_type
        )
        return response.embeddings

    async def store_embeddings(self, texts: List[str], metadata_list: List[Dict[str, Any]], model: str = "embed-english-v3.0"):
        """
        Generate and store embeddings in Qdrant with associated metadata.
        
        Args:
            texts: List of text strings to embed
            metadata_list: List of metadata dictionaries for each text
            model: Cohere embedding model to use
            
        Returns:
            List of IDs assigned to the stored embeddings
        """
        # Generate embeddings
        embeddings = self.generate_embeddings(texts, model)
        
        # Prepare points for Qdrant
        points = []
        ids = []
        
        for i, (text, embedding, metadata) in enumerate(zip(texts, embeddings, metadata_list)):
            point_id = str(uuid.uuid4())
            ids.append(point_id)
            
            point = models.PointStruct(
                id=point_id,
                vector=embedding,
                payload={
                    "content": text,
                    **metadata  # Include all metadata fields
                }
            )
            points.append(point)
        
        # Store in Qdrant
        self.qdrant_client.upsert(
            collection_name=self.qdrant_collection,
            points=points
        )
        
        return ids

    async def update_embedding(self, point_id: str, new_text: str, new_metadata: Dict[str, Any], model: str = "embed-english-v3.0"):
        """
        Update an existing embedding in Qdrant.
        
        Args:
            point_id: ID of the point to update
            new_text: New text content
            new_metadata: New metadata dictionary
            model: Cohere embedding model to use
        """
        # Generate new embedding
        new_embedding = self.generate_embeddings([new_text], model)[0]
        
        # Update the point in Qdrant
        self.qdrant_client.upsert(
            collection_name=self.qdrant_collection,
            points=[
                models.PointStruct(
                    id=point_id,
                    vector=new_embedding,
                    payload={
                        "content": new_text,
                        **new_metadata
                    }
                )
            ]
        )

    async def delete_embedding(self, point_id: str):
        """
        Delete an embedding from Qdrant.
        
        Args:
            point_id: ID of the point to delete
        """
        self.qdrant_client.delete(
            collection_name=self.qdrant_collection,
            points_selector=models.PointIdsList(
                points=[point_id]
            )
        )

    def get_embedding_dimension(self, model: str = "embed-english-v3.0") -> int:
        """
        Get the dimension of embeddings for a given model.
        
        Args:
            model: Cohere embedding model to check
            
        Returns:
            Dimension of the embeddings
        """
        # For Cohere's embed-english-v3.0, the dimension is typically 1024
        # This is a simplified implementation - in practice, you might need to check the model info
        return 1024