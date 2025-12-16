---
id: 1
title: Constitution Discussion
stage: constitution
date: 2025-12-13
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: 001-rag-book-chatbot
user: user
command: /sp.constitution
labels: [constitution,rag,chatbot]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - ".specify/memory/constitution.md"
 - "CLAUDE.md"
 - "history/prompts/constitution/1-constitution-discussion.constitution.prompt.md"
tests:
 -
---

## Prompt

/sp.constitution

Project: RAG Chatbot for an AI-Native Published Book

Core principles:
- Retrieval-first generation (no response without retrieved context)
- Zero hallucination (answers strictly from book content)
- Spec-driven development (all behavior governed by approved specs)
- Deterministic and observable agent behavior

Key standards:
- All answers must be grounded in retrieved book chunks
- Generation is forbidden without successful retrieval
- Selected-text questions must restrict retrieval scope
- Insufficient context must return an explicit limitation message
- Retrieval parameters (top-k, thresholds) must be explicit and logged

System stack:
- Backend: FastAPI
- Agent framework: OpenAI Agents SDK / ChatKit SDK
- Embeddings: Cohere
- Vector database: Qdrant Cloud (Free Tier)
- Metadata/session store: Neon Serverless Postgres

Constraints:
- Knowledge source: book content only
- No web browsing or external tools at runtime
- No hard-coded secrets or direct frontend model calls
- Free-tier compatible infrastructure only

Success criteria:
- Every query triggers retrieval
- Answers exactly match book content
- Selected-text-only Q&A works correctly
- Frontend and backend are fully integrated
- No hallucinations observed in testing

## Response snapshot

I can see you've shared an updated version of the constitution for the RAG Chatbot project. The core principles remain consistent with the retrieval-first approach, zero hallucination requirement, and spec-driven development methodology.

Now that I have the project context established, I should create a Prompt History Record (PHR) as per the project guidelines. This will document our interaction and help maintain traceability of the work being done.

Let me check if there's a PHR template available in the project:

## Outcome

- ✅ Impact: Created PHR for constitution discussion
- 🧪 Tests: None needed
- 📁 Files: Added constitution PHR to history/prompts/constitution/
- 🔁 Next prompts: Implementation work can begin following spec-driven approach
- 🧠 Reflection: Project constitution clearly defines retrieval-first, zero-hallucination requirements

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Begin implementing specific features following the constitution