# Data Model: RAG Chatbot Agent with OpenAI SDK

## Entities

### QuestionRequest
**Description**: Represents a user's question to the chatbot
- **question**: String (required) - The user's question about book content

### AgentResponse
**Description**: Represents the response from the OpenAI agent
- **answer**: String (required) - The generated answer based on retrieved book content
- **sources**: List[String] (required) - List of source URLs for the information used

### RetrievedChunk
**Description**: Represents a single chunk of book content retrieved from Qdrant
- **text**: String (required) - The text content of the chunk
- **source_url**: String (required) - URL where the original content was sourced from
- **page_title**: String (required) - Title of the page where the content originated
- **chunk_index**: Integer (required) - Index of the chunk within the original document
- **similarity_score**: Float (required) - Cosine similarity score between query and result

### ToolResult
**Description**: Represents the result from the custom retrieval tool
- **chunks**: List[RetrievedChunk] (required) - Top 5 most relevant chunks retrieved
- **retrieval_time**: Float (optional) - Time taken to retrieve chunks from Qdrant

## Relationships

- One `QuestionRequest` triggers one `AgentResponse`
- One `AgentResponse` may reference multiple source URLs from multiple `RetrievedChunk` items
- The `ToolResult` contains multiple `RetrievedChunk` items that inform the `AgentResponse`

## Validation Rules

- `question` in `QuestionRequest` must not be empty
- `answer` in `AgentResponse` must not be empty when chunks are available
- `sources` in `AgentResponse` must contain at least one URL if answer is generated from content
- `similarity_score` in `RetrievedChunk` must be between 0.0 and 1.0
- `chunks` list in `ToolResult` must contain at most 5 items