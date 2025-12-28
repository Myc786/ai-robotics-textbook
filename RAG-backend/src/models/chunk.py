from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import uuid


class ChunkBase(BaseModel):
    book_id: uuid.UUID
    chapter_id: uuid.UUID
    section_id: uuid.UUID
    content: str
    token_count: Optional[int] = None
    vector_id: Optional[str] = None  # ID in Qdrant


class ChunkCreate(ChunkBase):
    pass


class ChunkUpdate(BaseModel):
    content: Optional[str] = None
    token_count: Optional[int] = None
    vector_id: Optional[str] = None


class Chunk(ChunkBase):
    chunk_id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True