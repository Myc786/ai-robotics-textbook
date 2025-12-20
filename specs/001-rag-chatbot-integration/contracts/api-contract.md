# API Contract: RAG Chatbot Integration

**Feature**: RAG Chatbot Integration
**Created**: 2025-12-17
**Version**: 1.0

## Core Functions

### 1. get_all_urls(base_url: str) -> list[str]

**Purpose**: Discover and return all book page URLs from the provided base URL

**Parameters**:
- `base_url` (string): The base URL of the deployed book website (required)

**Returns**:
```json
{
  "urls": [
    string
  ],
  "total_count": integer,
  "base_url": string,
  "sitemap_url": string
}
```

**Process**:
- Will attempt to discover URLs from the sitemap at: https://ai-robotics-textbook.vercel.app/sitemap.xml
- Will fall back to web crawling if sitemap is not available or incomplete

**Errors**:
- `NetworkError`: When the base URL is inaccessible
- `URLDiscoveryError`: When URLs cannot be discovered from the page

**Example**:
```python
result = get_all_urls("https://ai-robotics-textbook.vercel.app/")
# Returns: {
#   "urls": [
#     "https://ai-robotics-textbook.vercel.app/chapter1",
#     "https://ai-robotics-textbook.vercel.app/chapter2"
#   ],
#   "total_count": 2,
#   "base_url": "https://ai-robotics-textbook.vercel.app/",
#   "sitemap_url": "https://ai-robotics-textbook.vercel.app/sitemap.xml"
# }
```

### 2. extract_text_from_url(url: str) -> dict

**Purpose**: Extract clean text content from a given URL

**Parameters**:
- `url` (string): The URL to extract content from (required)

**Returns**:
```json
{
  "success": bool,
  "content": string,
  "title": string,
  "metadata": {
    "url": string,
    "source_type": string,
    "content_length": integer,
    "fetch_time": string
  },
  "error": string (optional)
}
```

**Errors**:
- `NetworkError`: When the URL is inaccessible
- `ContentExtractionError`: When content cannot be extracted from the page

**Example**:
```python
result = extract_text_from_url("https://ai-robotics-textbook.vercel.app/chapter1")
# Returns: {
#   "success": true,
#   "content": "Chapter 1 content here...",
#   "title": "Introduction to AI",
#   "metadata": {
#     "url": "https://ai-robotics-textbook.vercel.app/chapter1",
#     "source_type": "webpage",
#     "content_length": 2450,
#     "fetch_time": "2025-12-17T10:30:00Z"
#   }
# }
```

### 3. chunk_text(content: str, chunk_size: int = 1000, overlap: int = 200) -> list[dict]

**Purpose**: Split content into manageable chunks with metadata

**Parameters**:
- `content` (string): The text content to chunk (required)
- `chunk_size` (integer): Size of each chunk (default: 1000)
- `overlap` (integer): Number of characters to overlap between chunks (default: 200)

**Returns**:
```json
{
  "chunks": [
    {
      "text": string,
      "chunk_index": integer,
      "original_length": integer
    }
  ],
  "chunk_count": integer,
  "original_length": integer
}
```

**Errors**: None

**Example**:
```python
result = chunk_text("Long text content...", 1000, 200)
# Returns: {
#   "chunks": [
#     {
#       "text": "First chunk of text...",
#       "chunk_index": 0,
#       "original_length": 2450
#     },
#     {
#       "text": "Second chunk with overlap...",
#       "chunk_index": 1,
#       "original_length": 2450
#     }
#   ],
#   "chunk_count": 2,
#   "original_length": 2450
# }
```

### 4. embed(texts: list[str]) -> list[list[float]]

**Purpose**: Generate embeddings for text chunks using Cohere

**Parameters**:
- `texts` (list[string]): List of text chunks to embed (required)

**Returns**:
```json
{
  "vectors": [
    list[float]
  ],
  "model": string,
  "text_count": integer
}
```

**Errors**:
- `EmbeddingGenerationError`: When the embedding service fails

**Example**:
```python
result = embed(["First chunk...", "Second chunk..."])
# Returns: {
#   "vectors": [
#     [0.1, 0.5, -0.3, ...],
#     [0.2, -0.1, 0.4, ...]
#   ],
#   "model": "embed-multilingual-v2.0",
#   "text_count": 2
# }
```

### 5. create_collection(collection_name: str = "RAG_embedding") -> bool

**Purpose**: Create or verify the existence of the Qdrant collection

**Parameters**:
- `collection_name` (string): Name for the vector collection (default: "RAG_embedding")

**Returns**:
```json
{
  "success": bool,
  "collection_name": string,
  "created": bool
}
```

**Errors**:
- `CollectionCreationError`: When the collection cannot be created

**Example**:
```python
result = create_collection("RAG_embedding")
# Returns: {
#   "success": true,
#   "collection_name": "RAG_embedding",
#   "created": true
# }
```

### 6. save_chunk_to_qdrant(chunk_data: dict, vector: list[float]) -> bool

**Purpose**: Store a single chunk with its embedding in Qdrant

**Parameters**:
- `chunk_data` (dict): Chunk data with metadata
- `vector` (list[float]): Embedding vector for the chunk

**Returns**:
```json
{
  "success": bool,
  "chunk_id": string
}
```

**Errors**:
- `StorageError`: When the vector database is unavailable

**Example**:
```python
chunk_data = {
  "text": "Sample chunk text...",
  "url": "https://ai-robotics-textbook.vercel.app/chapter1",
  "title": "Introduction",
  "chunk_index": 0
}
vector = [0.1, 0.5, -0.3, ...]
result = save_chunk_to_qdrant(chunk_data, vector)
# Returns: {
#   "success": true,
#   "chunk_id": "chunk-abc123"
# }
```

### 7. main() -> None

**Purpose**: Execute the complete RAG pipeline

**Parameters**: None (reads from command line arguments or configuration)

**Process**:
1. Initialize configuration and API clients
2. Discover all URLs from the target website
3. Process each URL: extract text → chunk → embed → save to Qdrant
4. Report progress and final status

**Example**:
```python
main()
# Processes all pages from "https://ai-robotics-textbook.vercel.app/"
# and stores embeddings in "RAG_embedding" collection
```

## CLI Interface

### Command: `python main.py index`

**Purpose**: Run the complete indexing pipeline

**Arguments**:
- `--target-url` (string): Base URL of the book website to index (required)
- `--chunk-size` (integer): Size of text chunks (default: 1000)
- `--overlap` (integer): Overlap between chunks (default: 200)
- `--collection` (string): Qdrant collection name (default: "RAG_embedding")

**Example**:
```bash
python main.py index --target-url "https://ai-robotics-textbook.vercel.app/" --chunk-size 1000 --overlap 200
```

**Output**:
- Progress indicators during processing
- Summary of indexed documents
- Error reports if any failures occur

### Command: `python main.py status`

**Purpose**: Check the status of the indexing process and vector database

**Arguments**: None

**Example**:
```bash
python main.py status
```

**Output**:
- Connection status to Cohere and Qdrant
- Number of indexed documents
- Health status of services

## Error Handling Contract

### Standard Error Response Format
```json
{
  "success": false,
  "error": {
    "type": string,
    "message": string,
    "details": object (optional)
  }
}
```

### Error Types
- `NetworkError`: Issues with fetching content from URLs
- `ContentExtractionError`: Problems extracting text from HTML
- `EmbeddingGenerationError`: Issues with the embedding service
- `StorageError`: Problems storing data in the vector database
- `ValidationError`: Input validation failures
- `ConfigurationError`: Missing or invalid configuration

## Performance Contract

### Expected Response Times
- `fetch_content`: < 5 seconds per URL (under normal network conditions)
- `chunk_text`: < 0.1 seconds per document
- `generate_embeddings`: < 2 seconds per batch of 10 chunks
- `store_embeddings`: < 1 second per batch of 10 entries

### Resource Usage
- Memory: < 500MB for processing 100 pages
- Concurrent API requests: Maximum 5 to respect rate limits