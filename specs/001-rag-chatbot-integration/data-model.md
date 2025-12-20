# Data Model: RAG Chatbot Integration

**Feature**: RAG Chatbot Integration
**Created**: 2025-12-17

## Entity Definitions

### BookContent
Represents the raw content extracted from educational book websites.

**Fields**:
- `id` (string): Unique identifier for the content item
- `url` (string): Source URL of the content (required, valid URL format)
- `title` (string): Title of the document/chapter (required, max 500 chars)
- `content` (string): Extracted text content (required, min 10 chars)
- `source_type` (string): Type of source (e.g., "webpage", "pdf", "html")
- `created_at` (datetime): Timestamp when content was indexed
- `updated_at` (datetime): Timestamp when content was last updated
- `content_length` (integer): Length of the extracted content in characters
- `metadata` (dict): Additional document metadata (optional)

**Validation Rules**:
- URL must be a valid, accessible web address
- Content must be at least 10 characters long
- Title must not exceed 500 characters

### Embedding
Represents the vector embedding of content for semantic similarity computation.

**Fields**:
- `id` (string): Unique identifier for the embedding
- `content_id` (string): Reference to the source BookContent item
- `vector` (list[float]): Numerical embedding representation (required)
- `model` (string): Name of the embedding model used
- `created_at` (datetime): Timestamp when embedding was generated
- `chunk_index` (integer): Index of this chunk within the original document
- `chunk_text` (string): The text that was embedded (first 1000 chars)

**Validation Rules**:
- Vector must have consistent dimensions based on the model
- Content_id must reference an existing BookContent item
- Chunk_index must be non-negative

### KnowledgeBaseEntry
Represents an indexed entry in the vector database with content and metadata.

**Fields**:
- `id` (string): Unique identifier for the knowledge base entry
- `payload` (dict): Content and metadata stored with the vector
  - `url` (string): Source URL
  - `title` (string): Document title
  - `content` (string): Content text (potentially truncated)
  - `source_type` (string): Type of source
  - `content_id` (string): Reference to BookContent
  - `chunk_index` (integer): Index of this chunk
- `vector` (list[float]): The embedding vector
- `created_at` (datetime): Timestamp when entry was stored

**Validation Rules**:
- Payload must contain required fields (url, title, content_id)
- Vector must match expected dimensions
- ID must be unique within the collection

## Relationships

### BookContent → Embedding
- One-to-Many relationship
- One BookContent item can generate multiple Embedding items if the content is chunked
- Embedding.content_id references BookContent.id

### Embedding → KnowledgeBaseEntry
- One-to-One relationship
- Each Embedding corresponds to one KnowledgeBaseEntry
- The embedding vector is stored directly in the KnowledgeBaseEntry

## State Transitions

### BookContent States
1. `FETCHED` - Content has been retrieved from the URL
2. `CLEANED` - Content has been processed and cleaned
3. `CHUNKED` - Content has been split into processable chunks
4. `INDEXED` - Content chunks have been embedded and stored

### Processing Flow
```
FETCHED → CLEANED → CHUNKED → INDEXED
```

Each state transition is associated with specific validation and error handling.

## Collection/Database Schema

### Qdrant Collection: "book_embeddings"
- **Vector Configuration**:
  - Size: 1024 (for Cohere embeddings)
  - Distance: Cosine
- **Payload Schema**:
  - url: keyword
  - title: text
  - content: text
  - content_id: keyword
  - chunk_index: integer
  - source_type: keyword
  - created_at: datetime

## Indexing Strategy

### Primary Indexes
- Content ID: For referencing original content
- URL: For identifying source documents
- Creation timestamp: For freshness tracking

### Search Optimization
- Vector index for similarity search
- Keyword indexes for metadata filtering
- Text index for content search capabilities