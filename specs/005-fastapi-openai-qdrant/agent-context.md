# Agent Context: FastAPI Backend with OpenAI Agent and Qdrant Retrieval

**Feature**: 005-fastapi-openai-qdrant
**Created**: 2025-12-19
**Technologies Added**: FastAPI, OpenAI Agent, Qdrant, Cohere, uv

## Technology Stack

### FastAPI
- Modern, fast web framework for building APIs with Python 3.7+
- Provides automatic API documentation with Swagger UI and ReDoc
- Built-in validation for request/response handling

### OpenAI Agent
- AI system that can use tools to perform actions
- Used for generating responses based on retrieved content
- Enforced to only use provided book content with system prompt

### Qdrant Vector Database
- Vector similarity search engine
- Used for semantic search of book content
- Efficient retrieval of relevant content chunks

### Cohere Embeddings
- Text embedding service for semantic search
- Converts text to vector representations
- Used for querying Qdrant vector database

### UV Package Manager
- Fast Python package installer and resolver
- Used for dependency management
- Provides virtual environment functionality

## Integration Pattern

The system follows a RAG (Retrieval-Augmented Generation) pattern:
1. User question → Cohere embedding → Qdrant search
2. Retrieved content → OpenAI agent → Generated response
3. Response with source citations returned to user