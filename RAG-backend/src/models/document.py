from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from datetime import datetime


class DocumentChunk(BaseModel):
    chunk_id: str
    document_id: str
    content: str
    url: Optional[str] = None
    chapter: Optional[str] = None
    section: Optional[str] = None
    page_number: Optional[int] = None
    metadata: Optional[Dict[str, Any]] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class Document(BaseModel):
    id: Optional[str] = None
    title: str
    author: Optional[str] = None
    url: Optional[str] = None
    source_type: str = "book"
    status: str = "indexed"
    total_chunks: int = 0
    indexed_chunks: int = 0
    metadata: Optional[Dict[str, Any]] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class RetrievedChunk(BaseModel):
    chunk_id: str
    content: str
    url: Optional[str] = None
    chapter: Optional[str] = None
    section: Optional[str] = None
    page_number: Optional[int] = None
    score: float
    metadata: Optional[Dict[str, Any]] = None


class QueryRequest(BaseModel):
    query: str
    selected_text: Optional[str] = None
    top_k: int = 5
    similarity_threshold: float = 0.5
    search_scope: str = "full_book"  # "full_book" or "selected_text_only"


class QueryResponse(BaseModel):
    query: str
    response: str
    retrieved_chunks: List[RetrievedChunk]
    response_status: str  # "success", "insufficient_context", "error"
    execution_time_ms: Optional[int] = None


class ChatSession(BaseModel):
    session_id: str
    user_id: Optional[str] = None
    created_at: datetime
    updated_at: datetime