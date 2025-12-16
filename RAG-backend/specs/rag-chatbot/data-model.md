# Data Model: RAG Chatbot

## Overview
Database schema and data structures for the RAG chatbot system, focusing on document chunks for vector storage and metadata/session tracking in Postgres.

## Vector Database (Qdrant) Schema

### Document Chunks Collection
The primary collection for vector search containing book content chunks with metadata.

**Collection Name**: `document_chunks`

**Vector Configuration**:
- Size: Depends on Cohere model (likely 1024 for multilingual-light-v2.0)
- Distance: Cosine

**Payload Fields**:
```
{
  "chunk_id": "str",           // Unique identifier for the chunk
  "document_id": "str",        // Reference to original document
  "content": "str",            // The actual text content of the chunk
  "url": "str",                // Source URL/page of the content
  "chapter": "str",            // Chapter or section identifier
  "section": "str",            // Section within chapter
  "page_number": "int",        // Page number if applicable
  "created_at": "datetime",    // Timestamp of creation
  "updated_at": "datetime"     // Timestamp of last update
}
```

**Indexing**:
- Index on `document_id`, `chapter`, `section` for efficient filtering
- Payload indexes for metadata-based filtering

## Postgres Database Schema

### Document Chunks Table (Metadata Reference)
For tracking chunks that are stored in the vector database:

```sql
CREATE TABLE document_chunks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    chunk_id VARCHAR(255) UNIQUE NOT NULL,  -- Matches Qdrant payload
    document_id VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    url VARCHAR(500),
    chapter VARCHAR(255),
    section VARCHAR(255),
    page_number INTEGER,
    metadata JSONB,             -- Additional metadata as needed
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_document_chunks_doc_id ON document_chunks(document_id);
CREATE INDEX idx_document_chunks_chapter ON document_chunks(chapter);
CREATE INDEX idx_document_chunks_section ON document_chunks(section);
```

### Documents Table
For tracking complete documents/books:

```sql
CREATE TABLE documents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title VARCHAR(500) NOT NULL,
    author VARCHAR(255),
    url VARCHAR(500),
    source_type VARCHAR(100),   -- 'book', 'chapter', 'article', etc.
    status VARCHAR(50) DEFAULT 'indexed',  -- 'pending', 'indexing', 'indexed', 'failed'
    total_chunks INTEGER DEFAULT 0,
    indexed_chunks INTEGER DEFAULT 0,
    metadata JSONB,             -- Additional document-level metadata
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

### Conversations Table
For tracking user conversations and queries:

```sql
CREATE TABLE conversations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id VARCHAR(255),       -- Optional user identification
    session_id VARCHAR(255),    -- Session identifier
    query TEXT NOT NULL,
    selected_text TEXT,         -- Optional selected text for constrained search
    retrieval_params JSONB,     -- Parameters used for retrieval (top_k, threshold, etc.)
    retrieved_chunks JSONB[],   -- Array of chunk IDs or metadata retrieved
    response TEXT,              -- Generated response
    response_status VARCHAR(50), -- 'success', 'insufficient_context', 'error'
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_conversations_session ON conversations(session_id);
CREATE INDEX idx_conversations_user ON conversations(user_id);
```

### Chunk Retrieval Log Table
For detailed logging of retrieval operations:

```sql
CREATE TABLE retrieval_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    conversation_id UUID REFERENCES conversations(id),
    query_embedding VECTOR(1024),  -- Assuming Cohere multilingual-light-v2.0
    retrieved_chunks JSONB,        -- Details of retrieved chunks with scores
    similarity_threshold FLOAT,
    top_k INTEGER,
    search_scope VARCHAR(50),      -- 'full_book', 'selected_text_only'
    selected_text_filter TEXT,     -- The text used for constraining search
    retrieved_count INTEGER,
    execution_time_ms INTEGER,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

## Data Relationships

```
documents (1) ←→ (many) document_chunks
conversations (1) ←→ (many) retrieval_logs
```

## Pydantic Models

### Document Models
```python
from pydantic import BaseModel
from typing import Optional, Dict, Any
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
```

### Query and Response Models
```python
class QueryRequest(BaseModel):
    query: str
    selected_text: Optional[str] = None
    top_k: int = 5
    similarity_threshold: float = 0.5
    search_scope: str = "full_book"  # "full_book" or "selected_text_only"

class QueryResponse(BaseModel):
    query: str
    response: str
    retrieved_chunks: list[RetrievedChunk]
    response_status: str  # "success", "insufficient_context", "error"
    execution_time_ms: Optional[int] = None

class ChatSession(BaseModel):
    session_id: str
    user_id: Optional[str] = None
    created_at: datetime
    updated_at: datetime
```

## Migration Strategy

1. Initial schema setup with core tables
2. Add indexes for performance optimization
3. Implement audit trails for compliance
4. Add foreign key constraints where appropriate

## Security Considerations

- Encrypt sensitive data if needed
- Use parameterized queries to prevent injection
- Implement proper access controls
- Regular backup procedures