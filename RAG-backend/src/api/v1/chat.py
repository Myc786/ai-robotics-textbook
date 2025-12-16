from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
import time
import logging

from ...models.document import QueryRequest, QueryResponse
from ...services.rag_agent_service import rag_agent_service
from ...core.database import get_db_session
from ...core.logger import setup_logger

router = APIRouter()
logger = setup_logger(__name__)


@router.post("/chat", response_model=QueryResponse, summary="Process a chat query")
async def chat_endpoint(
    query_request: QueryRequest,
    db_session: AsyncSession = Depends(get_db_session)
):
    """
    Process a user query using the RAG system.

    This endpoint:
    1. Takes a user query and optional selected text
    2. Performs retrieval against the vector store
    3. Generates a grounded response using the retrieved context
    4. Returns the response with source attribution
    """
    try:
        logger.info(f"Received chat request: {query_request.query[:50]}...")

        # Record start time for performance tracking
        start_time = time.time()

        # Process the query through the RAG agent
        response = await rag_agent_service.process_query(query_request)

        # Calculate execution time
        execution_time_ms = int((time.time() - start_time) * 1000)
        response.execution_time_ms = execution_time_ms

        logger.info(f"Chat request processed successfully in {execution_time_ms}ms")

        # TODO: Store conversation in the database for history tracking
        # This would involve creating a ConversationDB record

        return response

    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        logger.error(f"Error processing chat request: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while processing your query"
        )


@router.post("/chat/debug", response_model=QueryResponse, summary="Debug chat query with detailed output")
async def debug_chat_endpoint(
    query_request: QueryRequest,
    include_chunks: bool = True,
    db_session: AsyncSession = Depends(get_db_session)
):
    """
    Debug endpoint that provides detailed output for the chat process.

    Includes additional information useful for debugging and understanding
    the retrieval and generation process.
    """
    try:
        logger.info(f"Received debug chat request: {query_request.query[:50]}...")

        # Record start time for performance tracking
        start_time = time.time()

        # Process the query through the RAG agent
        response = await rag_agent_service.process_query(query_request)

        # Calculate execution time
        execution_time_ms = int((time.time() - start_time) * 1000)
        response.execution_time_ms = execution_time_ms

        logger.info(f"Debug chat request processed successfully in {execution_time_ms}ms")

        # In debug mode, we might want to add additional metadata
        if not include_chunks:
            # This is just a placeholder - in a real implementation,
            # we might want to conditionally include retrieved chunks
            pass

        return response

    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        logger.error(f"Error processing debug chat request: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while processing your query"
        )