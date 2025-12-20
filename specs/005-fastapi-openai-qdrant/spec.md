# Feature Specification: FastAPI Backend with OpenAI Agent and Qdrant Retrieval

**Feature Branch**: `005-fastapi-openai-qdrant`
**Created**: 2025-12-19
**Status**: Draft
**Input**: User description: "Spec 3 - Build FastAPI backend with OpenAI Agent and Qdrant retrieval

- Use existing backend folder and UV environment
- Add dependencies: uv add fastapi uvicorn openai python-dotenv
- Update .env with OPENAI_API_KEY and existing Cohere/Qdrant keys
- In single file main.py: create FastAPI app
- Add CORS middleware to allow frontend origin
- Implement retrieval tool: query → Cohere embed → Qdrant search → return top 5 chunks as string
- Create OpenAI Agent with this retrieval tool and system prompt: "Answer only using the provided book content. Cite sources."
- Add POST /chat endpoint: accept {"question": "..."}, run agent, return {"answer": "...", "sources": [urls]}
- Run locally: uvicorn main:app --reload
- Test endpoint with curl/Postman using 5 real book questions
- Verify answers are accurate, grounded, and include correct source URLs"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Ask Questions About Book Content (Priority: P1)

A user wants to ask questions about the AI robotics textbook content and receive accurate, source-cited answers from the RAG system. The user sends a question to the backend API and receives a response with the answer and source references.

**Why this priority**: This is the core functionality that delivers value to users by providing intelligent answers based on the book content.

**Independent Test**: Can be fully tested by sending a question to the /chat endpoint and verifying the response contains a relevant answer and source citations.

**Acceptance Scenarios**:

1. **Given** the backend is running with indexed book content, **When** a user sends a question via POST to /chat endpoint, **Then** the system returns an accurate answer with source URLs cited
2. **Given** a user submits a question about book content, **When** the system processes the query using the OpenAI Agent, **Then** the response is grounded in the provided book content and includes proper citations

---

### User Story 2 - Integrate with Frontend Application (Priority: P2)

The frontend application needs to communicate with the backend to enable the RAG chat functionality. The frontend sends questions to the backend and displays the AI-generated responses.

**Why this priority**: Essential for the frontend to interact with the backend service and provide a complete user experience.

**Independent Test**: Can be tested by making CORS-enabled requests from a frontend origin to the backend and receiving proper responses.

**Acceptance Scenarios**:

1. **Given** the frontend application is running, **When** it sends a question to the backend API, **Then** the request is accepted and processed without CORS errors

---

### User Story 3 - Verify Answer Accuracy and Sources (Priority: P3)

A user wants to ensure that the answers provided by the system are accurate and properly sourced from the book content, not hallucinated information.

**Why this priority**: Critical for maintaining trust in the system's responses and ensuring educational value.

**Independent Test**: Can be tested by submitting questions with known answers in the book content and verifying the response accuracy and source citations.

**Acceptance Scenarios**:

1. **Given** a question with a known answer in the book content, **When** the system processes the query, **Then** the answer matches the book content and includes correct source URLs
2. **Given** a question about book content, **When** the system generates a response, **Then** the answer is grounded only in the provided book content without hallucination

---

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST provide a POST /chat endpoint that accepts a JSON object with a "question" field
- **FR-002**: System MUST return a JSON response with "answer" and "sources" fields when processing a question
- **FR-003**: System MUST implement a retrieval tool that uses Cohere embeddings to search Qdrant vector database
- **FR-004**: System MUST return the top 5 relevant content chunks from Qdrant search results
- **FR-005**: System MUST create an OpenAI Agent that uses the retrieval tool to answer questions
- **FR-006**: System MUST enforce that the agent only answers using provided book content and cites sources
- **FR-007**: System MUST implement CORS middleware to allow requests from the frontend origin
- **FR-008**: System MUST use environment variables for API keys (OPENAI_API_KEY, Cohere, Qdrant credentials)
- **FR-009**: System MUST handle errors gracefully and return appropriate error responses
- **FR-010**: System MUST be deployable using UV package manager with uvicorn server

### Key Entities

- **Question**: A user's query about the book content that needs to be answered by the system
- **Response**: The system's answer to the user's question, including the answer text and source citations
- **Retrieval Tool**: A component that performs semantic search on the Qdrant vector database using Cohere embeddings
- **OpenAI Agent**: An AI agent that processes questions using the retrieval tool and generates grounded responses

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users receive accurate answers to their questions within 10 seconds of submission
- **SC-002**: 95% of responses include proper source citations that reference the correct book content
- **SC-003**: System successfully handles 100 concurrent user requests without performance degradation
- **SC-004**: 90% of answers are grounded in the provided book content without hallucination
- **SC-005**: Frontend application can successfully communicate with the backend without CORS errors
- **SC-006**: System can be deployed and run locally using uvicorn with --reload flag