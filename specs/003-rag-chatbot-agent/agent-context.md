# Agent Context Update: RAG Chatbot Agent

## Technologies Added

### OpenAI Agents SDK
- **Library**: openai
- **Purpose**: Create intelligent agents with custom tools
- **Usage**: Build an agent that can call custom functions to retrieve information from Qdrant
- **Features**: Tool calling, function execution, response generation

### FastAPI Framework
- **Library**: fastapi
- **Purpose**: Web framework for building the API
- **Usage**: Create the /chat endpoint and handle HTTP requests/responses
- **Features**: Automatic API documentation, type validation, async support

### Environment Management
- **Library**: python-dotenv
- **Purpose**: Handle API keys and configuration securely
- **Usage**: Load environment variables from .env file
- **Features**: Secure configuration management

### Qdrant Integration
- **Library**: qdrant-client
- **Purpose**: Vector database for semantic search
- **Usage**: Store and search book content chunks with metadata
- **Features**: Cosine similarity search, efficient retrieval

### Cohere Integration
- **Library**: cohere
- **Purpose**: Generate embeddings for semantic search queries
- **Usage**: Convert text queries to vector embeddings for similarity search
- **Features**: High-quality embeddings for query-document similarity

## Implementation Notes
- Single file implementation: main.py
- Agent architecture: Custom retrieval tool with OpenAI integration
- Retrieval process: Query → Cohere embedding → Qdrant search → Top 5 chunks
- Response format: Answer with source attribution
- Validation: Prevent hallucination by restricting LLM to retrieved content only