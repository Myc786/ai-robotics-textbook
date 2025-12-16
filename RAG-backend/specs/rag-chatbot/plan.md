# Implementation Plan: RAG Chatbot for AI-Native Published Book

**Branch**: `001-rag-book-chatbot` | **Date**: 2025-12-13 | **Spec**: [specs/rag-chatbot/spec.md]

**Input**: Feature specification from `/specs/rag-chatbot/spec.md`

## Summary

A Retrieval-Augmented Generation (RAG) chatbot that answers user questions strictly using the published book content, supporting both full-book queries and selected-text-only queries. The system will enforce retrieval-first behavior with zero hallucination, using FastAPI backend, Cohere embeddings, Qdrant vector database, and Neon Postgres for metadata.

## Technical Context

**Language/Version**: Python 3.11
**Primary Dependencies**: FastAPI, OpenAI SDK, Cohere, Qdrant, SQLAlchemy
**Storage**: Qdrant Cloud (vector DB), Neon Serverless Postgres (metadata/session)
**Testing**: pytest
**Target Platform**: Linux server
**Project Type**: web - backend API service
**Performance Goals**: <500ms response time for typical queries
**Constraints**: <200ms p95 latency, Free tier resource limits, Zero hallucination
**Scale/Scope**: Single-user application initially, with scalability to multiple users

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- ✅ Retrieval First: System designed to require retrieval before any generation
- ✅ Zero Hallucination: Implementation will strictly validate retrieved content before generation
- ✅ Spec Enforcement: Following approved spec and planned tasks
- ✅ Deterministic & Observable: All retrieval parameters will be explicit and logged

## Project Structure

### Documentation (this feature)

```text
specs/rag-chatbot/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── models/
│   │   ├── __init__.py
│   │   ├── document_chunk.py       # Document chunk model with metadata
│   │   └── conversation.py         # Conversation/session tracking
│   ├── services/
│   │   ├── __init__.py
│   │   ├── embedding_service.py    # Cohere embedding operations
│   │   ├── vector_store_service.py # Qdrant operations
│   │   ├── retrieval_service.py    # Main retrieval logic
│   │   └── rag_agent_service.py    # Agent logic with grounding checks
│   ├── api/
│   │   ├── __init__.py
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── chat.py            # Chat endpoints
│   │       └── documents.py       # Document upload/indexing endpoints
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py              # Configuration and settings
│   │   └── logger.py              # Logging setup
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── text_splitter.py       # Text chunking utilities
│   │   └── validators.py          # Request/response validation
│   └── main.py                    # Application entry point
├── tests/
│   ├── unit/
│   │   ├── models/
│   │   ├── services/
│   │   └── api/
│   ├── integration/
│   │   ├── api/
│   │   └── services/
│   └── conftest.py
├── requirements.txt
├── alembic/
│   └── versions/                  # Database migration scripts
├── alembic.ini
├── Dockerfile
└── docker-compose.yml
```

**Structure Decision**: Backend-only structure with FastAPI, following the web application pattern with separate concerns for models, services, API, and core configurations.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| N/A | N/A | N/A |
