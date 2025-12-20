# Data Model: RAG Book Content Retrieval

## Entities

### QueryRequest
**Description**: Represents a search query from the user
- **query_text**: String (required) - The user's search query
- **top_k**: Integer (default: 10) - Number of results to return
- **min_similarity**: Float (default: 0.75) - Minimum cosine similarity threshold

### SearchResult
**Description**: Represents a single search result from Qdrant
- **text**: String (required) - The original text content of the chunk
- **similarity_score**: Float (required) - Cosine similarity score between query and result
- **source_url**: String (required) - URL where the original content was sourced from
- **page_title**: String (required) - Title of the page where the content originated
- **chunk_index**: Integer (required) - Index of the chunk within the original document
- **metadata**: Dict (optional) - Additional metadata from Qdrant

### RetrievalResponse
**Description**: Represents the complete response to a retrieval request
- **query**: String (required) - The original query text
- **results**: List[SearchResult] (required) - List of search results, sorted by similarity
- **execution_time**: Float (required) - Time taken to execute the search in seconds
- **total_candidates**: Integer (optional) - Total number of candidates considered

## Relationships

- One `QueryRequest` produces one `RetrievalResponse`
- One `RetrievalResponse` contains multiple `SearchResult` items
- Each `SearchResult` corresponds to one vector in the Qdrant collection

## Validation Rules

- `similarity_score` must be between 0.0 and 1.0
- `top_k` must be between 1 and 100
- `min_similarity` must be between 0.0 and 1.0
- `query_text` must not be empty
- `results` list must contain at most `top_k` items
- All `SearchResult` items in a `RetrievalResponse` must have `similarity_score` >= `min_similarity`