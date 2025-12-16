import openai
from typing import List, Optional
import logging
from ..models.document import QueryRequest, QueryResponse, RetrievedChunk
from ..services.retrieval_service import retrieval_service
from ..core.config import settings
from ..core.logger import setup_logger

# Import Google Generative AI
try:
    import google.generativeai as genai
    GOOGLE_GENAI_AVAILABLE = True
except ImportError:
    GOOGLE_GENAI_AVAILABLE = False
    genai = None


class RAGAgentService:
    def __init__(self):
        self.logger = setup_logger(__name__)

        # Configure Google Generative AI if API key is available
        if settings.google_api_key and GOOGLE_GENAI_AVAILABLE:
            genai.configure(api_key=settings.google_api_key)
            self.gemini_model = genai.GenerativeModel('gemini-1.5-pro')  # Updated to use newer model
            self.logger.info("Google Generative AI configured successfully")
        else:
            self.gemini_model = None
            self.logger.warning("Google API key not set or library not available, using simulated response generation")

        # Note: Using OpenAI client as fallback; in a real implementation,
        # you might use a different LLM provider or the OpenAI Agents SDK
        if settings.openai_api_key:
            self.openai_client = openai.AsyncOpenAI(api_key=settings.openai_api_key)
        else:
            self.openai_client = None

    async def generate_response(
        self,
        query: str,
        retrieved_chunks: List[RetrievedChunk],
        context_sufficient: bool = True
    ) -> str:
        """
        Generate a response based only on the retrieved context.

        Args:
            query: The original user query
            retrieved_chunks: List of retrieved chunks with relevant information
            context_sufficient: Whether the retrieved context is sufficient

        Returns:
            Generated response string
        """
        try:
            if not context_sufficient or not retrieved_chunks:
                return "I cannot answer this question based on the available book content. The provided context does not contain sufficient information to answer your query."

            # Use Google Gemini API if available, otherwise fall back to simulated response
            if self.gemini_model:
                response = await self._generate_with_gemini(query, retrieved_chunks)
            else:
                # In a real implementation, we would use the OpenAI Agents SDK or similar
                # For now, we'll simulate the response generation with a simple approach
                # that ensures we only use the provided context
                response = self._generate_contextual_response(query, retrieved_chunks)

            return response

        except Exception as e:
            self.logger.error(f"Error generating response: {str(e)}")
            raise

    def _generate_contextual_response(
        self,
        query: str,
        retrieved_chunks: List[RetrievedChunk]
    ) -> str:
        """
        Generate a response based on the query and retrieved chunks.
        This is a simplified implementation that constructs a response from the context.
        In a production system, this would use an LLM with proper grounding checks.
        """
        # Combine all retrieved content
        all_content = " ".join([chunk.content for chunk in retrieved_chunks])

        # This is a simplified response generation
        # In a real implementation, we'd use an LLM with proper grounding validation
        response_parts = [
            f"I found the following information in the book related to your query: '{query}':"
        ]

        for i, chunk in enumerate(retrieved_chunks):
            response_parts.append(f"\nSource: {chunk.url or 'Unknown'}")
            response_parts.append(f"Content: {chunk.content[:200]}...")  # Truncate for brevity

        response_parts.append("\nThis information was retrieved from the book content provided.")

        return " ".join(response_parts)

    async def _generate_with_gemini(
        self,
        query: str,
        retrieved_chunks: List[RetrievedChunk]
    ) -> str:
        """
        Generate a response using Google Gemini based on the query and retrieved chunks.
        """
        try:
            # Construct context from retrieved chunks
            context_parts = []
            for chunk in retrieved_chunks:
                context_parts.append(f"Source: {chunk.url or 'Unknown'}")
                context_parts.append(f"Content: {chunk.content}")
                context_parts.append("---")

            context = "\n".join(context_parts)

            # Create a prompt that enforces using only the provided context
            prompt = f"""
            You are an AI assistant that answers questions based only on the provided book content.
            You must follow these rules strictly:
            1. Answer only using information from the provided context
            2. Do not use any external knowledge
            3. If the answer is not in the context, explicitly say so
            4. Always cite the source of information

            Context:
            {context}

            Question: {query}

            Answer:
            """

            # Generate content using Gemini
            response = await self.gemini_model.generate_content_async(prompt)

            # Extract text from the response
            if response and response.text:
                return response.text.strip()
            else:
                return "I found relevant information but couldn't generate a proper response. The provided context contains information about this topic."

        except Exception as e:
            self.logger.error(f"Error generating response with Gemini: {str(e)}")
            # Fall back to simulated response generation
            return self._generate_contextual_response(query, retrieved_chunks)

    async def process_query(
        self,
        query_request: QueryRequest
    ) -> QueryResponse:
        """
        Process a query request end-to-end: retrieve, evaluate, and generate response.

        Args:
            query_request: The query request with parameters

        Returns:
            QueryResponse with the answer and metadata
        """
        try:
            self.logger.info(f"Processing query: {query_request.query}")

            # Step 1: Retrieve relevant chunks
            retrieved_chunks = await retrieval_service.retrieve_relevant_chunks(
                query=query_request.query,
                top_k=query_request.top_k,
                similarity_threshold=query_request.similarity_threshold,
                selected_text=query_request.selected_text,
                search_scope=query_request.search_scope
            )

            # Step 2: Evaluate context sufficiency
            context_sufficient = await retrieval_service.evaluate_context_sufficiency(
                query=query_request.query,
                retrieved_chunks=retrieved_chunks
            )

            # Step 3: Generate response
            response_text = await self.generate_response(
                query=query_request.query,
                retrieved_chunks=retrieved_chunks,
                context_sufficient=context_sufficient
            )

            # Step 4: Create response object
            response = QueryResponse(
                query=query_request.query,
                response=response_text,
                retrieved_chunks=retrieved_chunks,
                response_status="success" if context_sufficient else "insufficient_context"
            )

            self.logger.info(f"Query processed successfully, context sufficient: {context_sufficient}")

            return response

        except Exception as e:
            self.logger.error(f"Error processing query: {str(e)}")

            # Return error response
            return QueryResponse(
                query=query_request.query,
                response="An error occurred while processing your query. Please try again.",
                retrieved_chunks=[],
                response_status="error"
            )


# Global instance of the RAG agent service
rag_agent_service = RAGAgentService()