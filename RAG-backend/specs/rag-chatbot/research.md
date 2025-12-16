# Research: RAG Chatbot Implementation

## Overview
Research document for implementing a Retrieval-Augmented Generation (RAG) chatbot that adheres to the project constitution of retrieval-first behavior and zero hallucination.

## Technology Stack Analysis

### FastAPI Backend
- Advantages: High-performance ASGI framework, excellent async support, automatic API documentation
- Relevant features: Pydantic models for validation, dependency injection, middleware support
- Libraries needed: fastapi, uvicorn, pydantic

### OpenAI Agents SDK / ChatKit SDK
- Need to determine which SDK to use based on requirements
- Both provide agent orchestration capabilities
- Will need to implement grounding checks to ensure responses only use retrieved content

### Cohere Embeddings
- Cohere provides high-quality text embeddings
- API key required for access
- Need to evaluate different model options (multilingual vs English-focused)

### Qdrant Cloud (Free Tier)
- Vector similarity search capabilities
- Cloud-hosted solution with free tier
- Need to consider rate limits and storage constraints of free tier
- Supports metadata filtering for selected-text-only queries

### Neon Serverless Postgres
- Serverless PostgreSQL with auto-scaling
- Good for metadata and session storage
- Need to design schema for document chunks, conversations, and metadata

## Architecture Components

### 1. Document Processing Pipeline
- Text ingestion from book content
- Chunking strategy for optimal retrieval
- Embedding generation and storage
- Metadata extraction and storage

### 2. Retrieval Service
- Vector similarity search in Qdrant
- Support for full-book and selected-text-only queries
- Context evaluation for sufficiency
- Explicit retrieval parameters (top-k, thresholds)

### 3. Agent Service
- Grounding validation before generation
- Response formatting with source attribution
- Fallback behavior when context insufficient
- Structured logging for observability

### 4. API Layer
- Endpoints for chat interactions
- Query validation and preprocessing
- Session/conversation management
- Error handling and response formatting

## Implementation Considerations

### Retrieval Parameters
- Top-k results: Default to 5-10 chunks for balance of relevance and context
- Similarity threshold: Minimum score to consider results relevant
- Chunk size: Balance between semantic coherence and information density

### Zero Hallucination Enforcement
- Implement strict validation that responses only contain information from retrieved chunks
- Create clear rejection messages when context is insufficient
- Log all retrieval results and decision points for auditability

### Selected-Text Restriction
- Implement metadata filters in Qdrant to constrain search to specific sections
- Validate that retrieved results match the requested scope
- Handle cases where no relevant content exists in selected text

## Security Considerations
- Secure API key storage using environment variables
- Input validation to prevent injection attacks
- Rate limiting to prevent abuse
- Proper authentication if needed for multi-user scenarios

## Testing Strategy
- Unit tests for individual services
- Integration tests for retrieval and generation pipeline
- Contract tests for API endpoints
- End-to-end tests for complete query flow