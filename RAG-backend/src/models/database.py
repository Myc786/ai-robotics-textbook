from sqlalchemy import Column, Integer, String, Text, DateTime, UUID, JSON, ARRAY, ForeignKey
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.sql import func
import uuid
from datetime import datetime


Base = declarative_base()


class DocumentChunkDB(Base):
    __tablename__ = "document_chunks"

    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    chunk_id = Column(String(255), unique=True, nullable=False, index=True)
    document_id = Column(String(255), nullable=False, index=True)
    content = Column(Text, nullable=False)
    url = Column(String(500))
    chapter = Column(String(255), index=True)
    section = Column(String(255), index=True)
    page_number = Column(Integer)
    metadata_ = Column(JSON)  # Additional metadata as needed (renamed from 'metadata' to avoid SQLAlchemy conflict)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class DocumentDB(Base):
    __tablename__ = "documents"

    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(500), nullable=False)
    author = Column(String(255))
    url = Column(String(500))
    source_type = Column(String(100))  # 'book', 'chapter', 'article', etc.
    status = Column(String(50), default='indexed')  # 'pending', 'indexing', 'indexed', 'failed'
    total_chunks = Column(Integer, default=0)
    indexed_chunks = Column(Integer, default=0)
    metadata_ = Column(JSON)  # Additional document-level metadata (renamed from 'metadata' to avoid SQLAlchemy conflict)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class ConversationDB(Base):
    __tablename__ = "conversations"

    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(String(255), index=True)  # Optional user identification
    session_id = Column(String(255), index=True)  # Session identifier
    query = Column(Text, nullable=False)
    selected_text = Column(Text)  # Optional selected text for constrained search
    retrieval_params = Column(JSON)  # Parameters used for retrieval (top_k, threshold, etc.)
    retrieved_chunks = Column(JSON)  # Array of chunk IDs or metadata retrieved
    response = Column(Text)  # Generated response
    response_status = Column(String(50))  # 'success', 'insufficient_context', 'error'
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class RetrievalLogDB(Base):
    __tablename__ = "retrieval_logs"

    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    conversation_id = Column(PG_UUID(as_uuid=True), ForeignKey("conversations.id"))
    # query_embedding would be stored as a vector in a real implementation
    retrieved_chunks = Column(JSON)  # Details of retrieved chunks with scores
    similarity_threshold = Column(Integer)
    top_k = Column(Integer)
    search_scope = Column(String(50))  # 'full_book', 'selected_text_only'
    selected_text_filter = Column(Text)  # The text used for constraining search
    retrieved_count = Column(Integer)
    execution_time_ms = Column(Integer)
    created_at = Column(DateTime(timezone=True), server_default=func.now())