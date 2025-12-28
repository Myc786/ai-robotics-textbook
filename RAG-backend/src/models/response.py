from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime
import uuid


class RetrievedChunk(BaseModel):
    chunk_id: str
    book_id: str
    chapter_id: str
    section_id: str
    content: str
    similarity_score: float


class ResponseBase(BaseModel):
    query_id: uuid.UUID
    response_text: str
    confidence_score: Optional[float] = None
    retrieved_chunks: Optional[List[Dict[str, Any]]] = None
    execution_time_ms: Optional[int] = None


class ResponseCreate(ResponseBase):
    pass


class ResponseUpdate(BaseModel):
    response_text: Optional[str] = None
    confidence_score: Optional[float] = None
    retrieved_chunks: Optional[List[Dict[str, Any]]] = None
    execution_time_ms: Optional[int] = None


class Response(ResponseBase):
    response_id: uuid.UUID
    created_at: datetime

    class Config:
        from_attributes = True