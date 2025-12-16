from typing import List, Optional, Dict, Any
from qdrant_client.http import models
from uuid import uuid4
import logging
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from src.core.vector_db import vector_db_client
from src.core.logger import setup_logger
from src.models.document import DocumentChunk


class VectorStoreService:
    def __init__(self):
        self.client = vector_db_client
        self.logger = setup_logger(__name__)
        self.collection_name = "Hackathon-Giaic"

    async def initialize_collection(self):
        """Initialize the document chunks collection in Qdrant with correct vector dimensions."""
        try:
            # Check if collection exists
            try:
                await self.client.get_collection_info(
                    collection_name=self.collection_name
                )
                self.logger.info(f"Collection '{self.collection_name}' already exists")
            except Exception:
                # Collection doesn't exist, create it with correct dimensions for embed-multilingual-v3.0 (1024)
                await self.client.create_collection_if_not_exists(
                    collection_name=self.collection_name,
                    vector_size=1024,  # Correct size for embed-multilingual-v3.0
                    distance="Cosine"
                )
                self.logger.info(f"Collection '{self.collection_name}' created with 1024 dimensions")
        except Exception as e:
            self.logger.error(f"Error initializing collection: {str(e)}")
            raise

    async def upsert_document_chunks(
        self,
        chunks: List[DocumentChunk],
        embeddings: List[List[float]]
    ):
        """
        Upsert document chunks with their embeddings to Qdrant.

        Args:
            chunks: List of DocumentChunk objects
            embeddings: List of embeddings corresponding to the chunks
        """
        try:
            # Create Qdrant points from document chunks
            points = []
            for chunk, embedding in zip(chunks, embeddings):
                # Convert chunk_id to UUID format as required by Qdrant
                import uuid
                point_id = str(uuid.uuid5(uuid.NAMESPACE_DNS, chunk.chunk_id))  # Generate UUID from chunk_id
                # Or use the original chunk_id if it's already a proper UUID
                try:
                    uuid.UUID(chunk.chunk_id)  # Test if it's already a valid UUID
                    point_id = chunk.chunk_id
                except ValueError:
                    # If not a valid UUID, generate one based on the chunk_id
                    point_id = str(uuid.uuid5(uuid.NAMESPACE_DNS, chunk.chunk_id))

                point = models.PointStruct(
                    id=point_id,
                    vector=embedding,
                    payload={
                        "chunk_id": chunk.chunk_id,
                        "document_id": chunk.document_id,
                        "content": chunk.content,
                        "url": chunk.url,
                        "chapter": chunk.chapter,
                        "section": chunk.section,
                        "page_number": chunk.page_number,
                        "metadata": chunk.metadata or {},
                        "created_at": chunk.created_at.isoformat() if chunk.created_at else None,
                        "updated_at": chunk.updated_at.isoformat() if chunk.updated_at else None
                    }
                )
                points.append(point)

            # Upsert points to Qdrant
            await self.client.upsert_vectors(
                collection_name=self.collection_name,
                points=points
            )

            self.logger.info(f"Successfully upserted {len(chunks)} chunks to Qdrant")

        except Exception as e:
            self.logger.error(f"Error upserting document chunks: {str(e)}")
            raise

    async def search(
        self,
        query_vector: List[float],
        top_k: int = 5,
        document_id: Optional[str] = None,
        chapter: Optional[str] = None,
        section: Optional[str] = None
    ) -> List[models.ScoredPoint]:
        """
        Search for similar chunks in the vector store.

        Args:
            query_vector: The query embedding vector
            top_k: Number of results to return
            document_id: Optional filter for specific document
            chapter: Optional filter for specific chapter
            section: Optional filter for specific section

        Returns:
            List of ScoredPoint objects from Qdrant
        """
        try:
            # Build filters if needed
            filters = []
            if document_id:
                filters.append(
                    models.FieldCondition(
                        key="document_id",
                        match=models.MatchValue(value=document_id)
                    )
                )
            if chapter:
                filters.append(
                    models.FieldCondition(
                        key="chapter",
                        match=models.MatchValue(value=chapter)
                    )
                )
            if section:
                filters.append(
                    models.FieldCondition(
                        key="section",
                        match=models.MatchValue(value=section)
                    )
                )

            # Create filter object if any filters exist
            filter_obj = None
            if filters:
                if len(filters) == 1:
                    filter_obj = models.Filter(must=[filters[0]])
                else:
                    filter_obj = models.Filter(must=filters)

            # Perform search
            results = await self.client.search_vectors(
                collection_name=self.collection_name,
                query_vector=query_vector,
                top_k=top_k,
                filters=filter_obj
            )

            self.logger.info(f"Found {len(results)} results for vector search")

            return results

        except Exception as e:
            self.logger.error(f"Error searching vector store: {str(e)}")
            raise

    async def delete_document_chunks(self, document_id: str):
        """
        Delete all chunks associated with a specific document.

        Args:
            document_id: ID of the document to delete chunks for
        """
        try:
            # Create filter for document_id
            filter_condition = models.Filter(
                must=[
                    models.FieldCondition(
                        key="document_id",
                        match=models.MatchValue(value=document_id)
                    )
                ]
            )

            # Delete points matching the filter
            await self.client.client.delete(
                collection_name=self.collection_name,
                points_selector=models.FilterSelector(
                    filter=filter_condition
                )
            )

            self.logger.info(f"Deleted chunks for document: {document_id}")

        except Exception as e:
            self.logger.error(f"Error deleting document chunks: {str(e)}")
            raise

    async def get_chunk_by_id(self, chunk_id: str) -> Optional[models.Record]:
        """
        Retrieve a single chunk by its ID.

        Args:
            chunk_id: ID of the chunk to retrieve

        Returns:
            The Record object or None if not found
        """
        try:
            records = await self.client.client.retrieve(
                collection_name=self.collection_name,
                ids=[chunk_id],
                with_payload=True,
                with_vectors=False
            )

            if records:
                return records[0]
            return None

        except Exception as e:
            self.logger.error(f"Error retrieving chunk by ID: {str(e)}")
            raise


# Global instance of the vector store service
vector_store_service = VectorStoreService()