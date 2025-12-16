---
id: 2
title: Specification Discussion
stage: spec
date: 2025-12-13
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: 001-rag-book-chatbot
user: user
command: //sp.specify
labels: [spec,rag,chatbot,requirements]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - "history/prompts/general/2-specification-discussion.general.prompt.md"
tests:
 -
---

## Prompt

//sp.specify

Project: RAG Chatbot for an AI-Native Published Book

Objective:
Design a Retrieval-Augmented Generation (RAG) chatbot that answers user questions strictly using the published book content, supporting both full-book queries and selected-text-only queries, and integrates seamlessly with the existing frontend.

System Behavior:
- The chatbot accepts a user query and optional selected text.
- The system performs retrieval against the book's vector index before any generation.
- The agent evaluates retrieved context for sufficiency.
- The system generates a grounded response or returns a clear limitation message.

Functional Requirements:
- Support global book search for general questions.
- Support selected-text-constrained search when user-highlighted text is provided.
- Enforce retrieval-first behavior for every query.
- Return responses grounded exclusively in retrieved book chunks.
- Include source metadata (URL, section, chunk ID) with each answer.

Non-Functional Requirements:
- Low-latency responses suitable for interactive use.
- Deterministic retrieval behavior with explicit parameters.
- Observable agent decisions through structured logging.
- Secure handling of API keys and credentials.

Technology Constraints:
- Backend framework: FastAPI
- Agent framework: OpenAI Agents SDK / ChatKit SDK
- Embedding model: Cohere
- Vector database: Qdrant Cloud (Free Tier)
- Metadata/session storage: Neon Serverless Postgres

Out of Scope:
- Book content creation or modification
- External web search or browsing
- Non-book knowledge sources

Acceptance Criteria:
- Every user query triggers a retrieval step.
- The chatbot never answers outside retrieved content.
- Selected-text-only questions restrict retrieval correctly.
- Clear refusal is returned when context is insufficient.
- Backend APIs are ready for frontend integration.

## Response snapshot

I'll create a Prompt History Record for this specification discussion as well:

## Outcome

- ✅ Impact: Created PHR for specification discussion
- 🧪 Tests: None needed
- 📁 Files: Added specification PHR to history/prompts/general/
- 🔁 Next prompts: Move to planning phase to design implementation approach
- 🧠 Reflection: Clear functional and non-functional requirements established for RAG chatbot

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Begin planning implementation of RAG system