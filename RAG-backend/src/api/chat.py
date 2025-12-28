from fastapi import APIRouter, HTTPException, Depends
from typing import Optional
import time
import uuid
from src.models.query import QueryCreate
from src.models.response import ResponseCreate, RetrievedChunk
from src.services.retrieval import RetrievalService
from src.services.generation import GenerationService
from src.services.ingestion import IngestionService
from src.services.validation import ValidationService
from src.config.database import postgres_db
from src.config.settings import settings


router = APIRouter()

# Initialize services
retrieval_service = RetrievalService()
generation_service = GenerationService()
ingestion_service = IngestionService()
validation_service = ValidationService()


async def log_to_database(query_data, response_data, context_chunks, execution_time):
    """Log query and response to database, silently fail if DB not available."""
    try:
        if postgres_db.connection is None:
            return

        query_id = uuid.uuid4()
        await postgres_db.connection.execute(
            """
            INSERT INTO queries (query_id, query_text, mode, selected_text)
            VALUES ($1, $2, $3, $4)
            """,
            query_id,
            query_data.query_text,
            query_data.mode,
            query_data.selected_text
        )

        await postgres_db.connection.execute(
            """
            INSERT INTO responses (response_id, query_id, response_text, confidence_score, retrieved_chunks, execution_time_ms)
            VALUES ($1, $2, $3, $4, $5, $6)
            """,
            uuid.uuid4(),
            query_id,
            response_data["response_text"],
            response_data["confidence_score"],
            context_chunks if context_chunks else [],
            int(execution_time * 1000)
        )
    except Exception as e:
        print(f"Warning: Failed to log to database: {e}")


@router.post("/chat")
async def chat_endpoint(query_data: QueryCreate):
    """
    Main chat endpoint for the RAG system.

    Args:
        query_data: Query with text, mode, and optional selected text

    Returns:
        Response with answer, retrieved chunks, confidence, and execution time
    """
    start_time = time.time()

    # Validate the query data
    validation_result = validation_service.validate_query_mode(
        query_data.query_text,
        query_data.mode,
        query_data.selected_text
    )

    if not validation_result["is_valid"]:
        raise HTTPException(status_code=400, detail=validation_result["errors"])

    try:
        # Determine if we're in selected-text mode
        if query_data.mode == "selected_text" and query_data.selected_text:
            # Use only the selected text for context
            context_chunks = [{
                "chunk_id": "selected_text",
                "book_id": "n/a",
                "chapter_id": "n/a",
                "section_id": "n/a",
                "content": query_data.selected_text,
                "similarity_score": 1.0
            }]
        else:
            # Use retrieval to find relevant chunks from the book
            context_chunks = await retrieval_service.retrieve_relevant_chunks(
                query_data.query_text
            )

            # Validate retrieval quality
            if not await retrieval_service.validate_retrieval_quality(
                query_data.query_text,
                context_chunks
            ):
                # If retrieval quality is poor, generate refusal response
                response_data = await generation_service.generate_refusal_response()
                execution_time = time.time() - start_time

                # Log the query and response in the database
                await log_to_database(query_data, response_data, response_data.get("retrieved_chunks", []), execution_time)

                return {
                    "response": response_data["response_text"],
                    "retrieved_chunks": response_data.get("retrieved_chunks", []),
                    "confidence": response_data["confidence_score"],
                    "execution_time_ms": int(execution_time * 1000)
                }

        # Generate response using the context
        response_data = await generation_service.generate_response(
            query_data.query_text,
            context_chunks
        )

        execution_time = time.time() - start_time

        # Validate response quality
        if not await generation_service.validate_response_quality(
            query_data.query_text,
            response_data["response_text"],
            context_chunks
        ):
            # If response quality is poor, return a refusal
            response_data = await generation_service.generate_refusal_response()

        # Validate that the answer is grounded in the provided context
        is_answer_valid = validation_service.validate_answer_content(
            response_data["response_text"],
            context_chunks[0]["content"] if context_chunks else ""
        )

        if not is_answer_valid:
            # If the answer is not properly grounded, return a refusal
            response_data = await generation_service.generate_refusal_response()

        # Log the query and response in the database
        await log_to_database(query_data, response_data, context_chunks, execution_time)

        return {
            "response": response_data["response_text"],
            "retrieved_chunks": [
                {
                    "chunk_id": chunk["chunk_id"],
                    "book_id": chunk["book_id"],
                    "chapter_id": chunk["chapter_id"],
                    "section_id": chunk["section_id"],
                    "content": chunk["content"],
                    "similarity_score": chunk["similarity_score"]
                }
                for chunk in context_chunks
            ],
            "confidence": response_data["confidence_score"],
            "execution_time_ms": int(execution_time * 1000)
        }

    except Exception as e:
        execution_time = time.time() - start_time
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/ingest")
async def ingest_endpoint(source: str, source_type: str, book_title: str, author: str = None):
    """
    Endpoint to ingest a book into the RAG system from various sources.

    Args:
        source: Path to the file, URL, or sitemap URL
        source_type: Type of source ('pdf', 'html', 'md', 'mdx', 'url', 'sitemap')
        book_title: Title of the book
        author: Author of the book (optional)

    Returns:
        Ingestion result
    """
    try:
        result = await ingestion_service.ingest_book(source, source_type, book_title, author)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))