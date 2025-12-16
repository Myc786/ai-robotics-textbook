from typing import List, Optional
from ..models.document import RetrievedChunk, QueryRequest
from ..services.embedding_service import embedding_service
from ..services.vector_store_service import vector_store_service
from ..core.logger import setup_logger
import logging


class RetrievalService:
    def __init__(self):
        self.logger = setup_logger(__name__)

    async def retrieve_relevant_chunks(
        self,
        query: str,
        top_k: int = 5,
        similarity_threshold: float = 0.5,
        selected_text: Optional[str] = None,
        search_scope: str = "full_book"
    ) -> List[RetrievedChunk]:
        """
        Retrieve relevant document chunks based on the query.

        Args:
            query: The user's query
            top_k: Number of top results to return
            similarity_threshold: Minimum similarity score to consider
            selected_text: Optional text to constrain search to specific section
            search_scope: "full_book" or "selected_text_only"

        Returns:
            List of RetrievedChunk objects
        """
        try:
            self.logger.info(f"Retrieving relevant chunks for query: {query[:50]}...")

            # Generate embedding for the query
            query_embedding = await embedding_service.embed_query(query)

            # Set up filters based on search scope and selected text
            document_id_filter = None
            chapter_filter = None
            section_filter = None

            if search_scope == "selected_text_only" and selected_text:
                # If searching in selected text only, we need to identify
                # the document/chapter/section that contains the selected text
                # For now, we'll use a simple approach and assume we know the context
                # In a real implementation, we'd need to map the selected text to its source
                self.logger.info("Constraining search to selected text context")
                # This is a simplified implementation - in practice, you'd need to identify
                # the specific document/chapter/section that contains the selected text

            # Perform search in vector store
            search_results = await vector_store_service.search(
                query_vector=query_embedding,
                top_k=top_k * 2,  # Get more results to account for filtering
                document_id=document_id_filter,
                chapter=chapter_filter,
                section=section_filter
            )

            # Convert search results to RetrievedChunk objects
            retrieved_chunks = []
            for result in search_results:
                # Apply similarity threshold filter
                if result.score >= similarity_threshold:
                    payload = result.payload
                    chunk = RetrievedChunk(
                        chunk_id=payload.get("chunk_id"),
                        content=payload.get("content", ""),
                        url=payload.get("url"),
                        chapter=payload.get("chapter"),
                        section=payload.get("section"),
                        page_number=payload.get("page_number"),
                        score=result.score,
                        metadata=payload.get("metadata", {})
                    )
                    retrieved_chunks.append(chunk)

            # Limit to top_k results after filtering
            retrieved_chunks = retrieved_chunks[:top_k]

            self.logger.info(f"Retrieved {len(retrieved_chunks)} relevant chunks")

            return retrieved_chunks

        except Exception as e:
            self.logger.error(f"Error in retrieval: {str(e)}")
            raise

    async def evaluate_context_sufficiency(
        self,
        query: str,
        retrieved_chunks: List[RetrievedChunk],
        minimum_chunks: int = 1,
        minimum_similarity: float = 0.3
    ) -> bool:
        """
        Evaluate if the retrieved context is sufficient to answer the query.

        Args:
            query: The original query
            retrieved_chunks: List of retrieved chunks
            minimum_chunks: Minimum number of chunks required
            minimum_similarity: Minimum similarity score required

        Returns:
            True if context is sufficient, False otherwise
        """
        # Check if we have enough chunks
        if len(retrieved_chunks) < minimum_chunks:
            self.logger.info(f"Insufficient chunks: {len(retrieved_chunks)} < {minimum_chunks}")
            return False

        # Check if the highest similarity score meets the threshold
        if retrieved_chunks and max(chunk.score for chunk in retrieved_chunks) < minimum_similarity:
            self.logger.info(f"Insufficient similarity: max score {max(chunk.score for chunk in retrieved_chunks)} < {minimum_similarity}")
            return False

        # Additional context evaluation could be implemented here
        # For example, checking if the chunks contain relevant information to the query

        self.logger.info("Context evaluation: Sufficient context available")
        return True


# Global instance of the retrieval service
retrieval_service = RetrievalService()