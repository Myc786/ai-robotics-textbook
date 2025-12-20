# Feature Specification: RAG Chatbot Agent with OpenAI SDK

**Feature Branch**: `003-rag-chatbot-agent`
**Created**: 2025-12-19
**Status**: Draft
**Input**: User description: "Integrate RAG Chatbot - Spec 3: Build Agent using OpenAI Agents SDK + FastAPI and add retrieval from Qdrant

Target audience: Developers who want a working backend that answers book questions using retrieved content
Focus: Create a simple, fast FastAPI server that receives a user question, uses OpenAI Agents SDK to call a retrieval tool, gets relevant book chunks from Qdrant, and returns a clean answer

Success criteria:
- FastAPI endpoint /chat accepts POST with {"question": "…"}
- Uses OpenAI Agents SDK to create one agent with a custom retrieval tool
- Tool calls Qdrant → gets top 5 chunks → passes them to the LLM
- LLM answers only using the retrieved book content (no hallucination)
- Returns JSON: {"answer": "…", "sources": [urls]}
- Runs locally with uvicorn

Constraints:
- Use same backend folder + UV project from Spec 1 & 2
- Technologies: FastAPI, OpenAI Agents SDK, python-dotenv, same Cohere + Qdrant clients
- Single main file: main.py (put everything in one file)
- Use your own OpenAI API key in .env
- Timeline: Complete in 1 day

Not building:
- Frontend integration (Spec 4)
- Authentication or rate limiting
- Conversation history / memory
- Neon Postgres (saved for later if needed)
- Fancy UI or streaming"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Answer Book Questions via API (Priority: P1)

As a developer, I want to send a question about book content to a FastAPI endpoint so that I receive a relevant answer generated from the retrieved book content. This enables me to test the RAG system's ability to answer questions based on the indexed book data.

**Why this priority**: This is the core functionality of the RAG chatbot - accepting user questions and returning accurate answers based on book content.

**Independent Test**: Can be fully tested by sending various questions to the /chat endpoint and verifying that the response contains a relevant answer based on the retrieved book content and a list of source URLs.

**Acceptance Scenarios**:

1. **Given** a running FastAPI server with the RAG agent, **When** I POST a question to the /chat endpoint, **Then** I receive a response with an answer generated from the retrieved book content and a list of source URLs
2. **Given** a question that requires information from multiple book sources, **When** I submit the question to the system, **Then** the answer incorporates information from multiple retrieved chunks and lists all relevant source URLs

---

### User Story 2 - Validate Retrieval-Based Answers (Priority: P1)

As a developer testing the RAG system, I want the LLM to answer only using the retrieved book content so that I can ensure the system doesn't hallucinate information. This validates that the answers are grounded in the actual book content.

**Why this priority**: This ensures the system provides reliable, factual answers based on the indexed content rather than generating incorrect information.

**Independent Test**: Can be tested by providing questions with specific book content and verifying that the answers contain information that matches the retrieved chunks and do not include fabricated details.

**Acceptance Scenarios**:

1. **Given** a question about specific book content, **When** the system retrieves relevant chunks and generates an answer, **Then** the answer contains only information present in the retrieved book content without hallucination
2. **Given** a question with no relevant content in the database, **When** the system processes the query, **Then** it responds appropriately acknowledging the lack of relevant information rather than making up answers

---

### User Story 3 - Access Source Information (Priority: P2)

As a developer validating the system, I want to receive source URLs with each answer so that I can verify where the information came from and validate the retrieval accuracy.

**Why this priority**: Source attribution is essential for verifying the quality and accuracy of the retrieved information.

**Independent Test**: Can be tested by examining the sources field in the response and confirming that the URLs correspond to the book content that was actually used in generating the answer.

**Acceptance Scenarios**:

1. **Given** a successful question response, **When** I examine the response data, **Then** the sources array contains valid URLs that correspond to the book content used in the answer

---

### Edge Cases

- What happens when the OpenAI API is unavailable during processing?
- How does the system handle extremely long questions that exceed token limits?
- What occurs when Qdrant is temporarily unavailable during retrieval?
- How does the system handle questions that have no relevant matches in the book content?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST provide a FastAPI endpoint /chat that accepts POST requests with a JSON payload containing a "question" field
- **FR-002**: System MUST use OpenAI Agents SDK to create an agent with a custom retrieval tool
- **FR-003**: The retrieval tool MUST call Qdrant and retrieve the top 5 most relevant book content chunks
- **FR-004**: System MUST pass the retrieved chunks to the LLM to generate an answer based only on the provided content
- **FR-005**: System MUST return a JSON response containing an "answer" field with the generated response and a "sources" field with an array of source URLs
- **FR-006**: System MUST prevent the LLM from hallucinating information not present in the retrieved book content
- **FR-007**: System MUST run locally using uvicorn for development and testing
- **FR-008**: System MUST be implemented in a single main.py file with clear separation of concerns using functions and classes

### Key Entities *(include if feature involves data)*

- **Question**: User input containing a query about book content, represented as a string
- **Retrieved Chunks**: Relevant text segments from book content with similarity scores and metadata (source URL, page title, chunk index)
- **Answer**: Generated response based on retrieved content, represented as a string
- **Source URLs**: List of URLs corresponding to the book content used in generating the answer

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: FastAPI endpoint /chat successfully accepts POST requests with question payload and returns responses within 10 seconds
- **SC-002**: OpenAI Agents SDK successfully creates an agent with a custom retrieval tool that integrates with Qdrant
- **SC-003**: Retrieval tool successfully fetches top 5 relevant chunks from Qdrant with appropriate similarity scores
- **SC-004**: LLM generates answers that contain information only from the retrieved book content without hallucination (measured by manual validation)
- **SC-005**: System returns complete JSON responses with both answer and sources fields populated correctly
- **SC-006**: Application runs successfully with uvicorn in a local development environment