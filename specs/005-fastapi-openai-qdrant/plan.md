# Implementation Plan: FastAPI Backend with OpenAI Agent and Qdrant Retrieval

**Feature**: 005-fastapi-openai-qdrant
**Created**: 2025-12-19
**Status**: Draft
**Branch**: 005-fastapi-openai-qdrant

## Technical Context

This feature involves building a FastAPI backend service that integrates with OpenAI's agent system and Qdrant vector database for Retrieval-Augmented Generation (RAG). The system will allow users to ask questions about AI robotics textbook content and receive accurate, source-cited answers.

The backend will use Cohere embeddings to search the Qdrant vector database, retrieve relevant content chunks, and pass them to an OpenAI agent with a specific system prompt to generate grounded responses. The service will include a POST /chat endpoint that accepts user questions and returns answers with source citations.

**Key Technologies**:
- FastAPI: Web framework for building the API
- OpenAI: Agent system for generating responses
- Qdrant: Vector database for content retrieval
- Cohere: Embedding generation for semantic search
- uv: Package manager and virtual environment
- uvicorn: ASGI server for running the application

**Unknowns**: None identified - all requirements are clear from the specification.

## Architecture & Design

### System Architecture
```
[Frontend] → [FastAPI Backend] → [Qdrant Vector DB]
                 ↓
            [OpenAI Agent]
                 ↓
            [Cohere Embeddings]
```

The system follows a microservice architecture where the FastAPI backend serves as the orchestrator between the frontend, OpenAI agent, and the Qdrant vector database. Cohere embeddings are used for semantic search to retrieve relevant content chunks.

### Data Flow
1. User submits a question via POST to /chat endpoint
2. Backend generates embeddings for the question using Cohere
3. Qdrant is queried with these embeddings to find top 5 relevant content chunks
4. OpenAI agent is invoked with the retrieved content and a system prompt
5. Agent generates an answer based only on the provided content
6. Response includes the answer text and source URLs
7. Response is returned to the frontend

## Implementation Approach

### Phase 0: Setup and Dependencies
1. Navigate to existing backend folder
2. Add required dependencies using uv:
   - fastapi
   - uvicorn
   - openai
   - python-dotenv
3. Update .env file with API keys (OPENAI_API_KEY, Cohere, Qdrant)

### Phase 1: Core Backend Implementation
1. Create single-file FastAPI application (main.py)
2. Implement CORS middleware configuration
3. Build retrieval tool function:
   - Accept query text
   - Generate Cohere embeddings
   - Search Qdrant for top 5 chunks
   - Return chunks as string
4. Create OpenAI Agent with:
   - Custom system prompt: "Answer only using the provided book content. Cite sources."
   - Retrieval tool integration

### Phase 2: API Endpoint and Testing
1. Implement POST /chat endpoint:
   - Accept JSON with "question" field
   - Process through OpenAI agent
   - Return JSON with "answer" and "sources" fields
2. Test locally with uvicorn --reload
3. Validate with 5 real book questions using curl/Postman
4. Verify answer accuracy and source citations

## Constitution Check

### Alignment with Project Principles
- ✅ Minimalism: Single-file implementation approach
- ✅ User Value: Provides accurate, source-cited answers to user questions
- ✅ Security: Uses environment variables for API keys
- ✅ Performance: Efficient vector search with Qdrant
- ✅ Maintainability: Clear separation of concerns in design

### Potential Violations
- None identified - all implementation approaches align with project principles

## Risk Analysis

### Technical Risks
1. **API Key Management**: Risk of exposing sensitive credentials
   - Mitigation: Use environment variables and secure .env file

2. **Response Accuracy**: Risk of hallucination or inaccurate answers
   - Mitigation: Strict system prompt enforcing use of only provided content

3. **Performance**: Risk of slow response times with large vector databases
   - Mitigation: Optimize Qdrant queries and implement caching if needed

### Implementation Risks
1. **Integration Complexity**: Risk of complexity in connecting multiple services
   - Mitigation: Clear interface definitions and error handling

2. **Dependency Management**: Risk of version conflicts
   - Mitigation: Use uv for consistent dependency management