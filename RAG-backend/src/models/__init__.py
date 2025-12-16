"""
Models package for the RAG Chatbot application.
"""
from .document import (
    DocumentChunk,
    Document,
    RetrievedChunk,
    QueryRequest,
    QueryResponse,
    ChatSession
)
from .database import (
    Base,
    DocumentChunkDB,
    DocumentDB,
    ConversationDB,
    RetrievalLogDB
)

__all__ = [
    # Pydantic models
    "DocumentChunk",
    "Document",
    "RetrievedChunk",
    "QueryRequest",
    "QueryResponse",
    "ChatSession",
    # SQLAlchemy models
    "Base",
    "DocumentChunkDB",
    "DocumentDB",
    "ConversationDB",
    "RetrievalLogDB"
]