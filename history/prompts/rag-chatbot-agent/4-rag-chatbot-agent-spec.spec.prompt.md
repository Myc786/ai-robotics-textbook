---
id: 4
title: rag-chatbot-agent-spec
stage: spec
date: 2025-12-19
surface: agent
model: claude-sonnet-4-5-20250929
feature: rag-chatbot-agent
branch: 003-rag-chatbot-agent
user: claude-code
command: /sp.specify
labels: [rag, chatbot, openai, fastapi, qdrant, agent]
links:
  spec: ../specs/003-rag-chatbot-agent/spec.md
  ticket: null
  adr: null
  pr: null
files:
 - ../specs/003-rag-chatbot-agent/spec.md
 - ../specs/003-rag-chatbot-agent/checklists/requirements.md
tests:
 - none
---

## Prompt

Integrate RAG Chatbot - Spec 3: Build Agent using OpenAI Agents SDK + FastAPI and add retrieval from Qdrant

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
- Fancy UI or streaming

## Response snapshot

Created a comprehensive specification for the RAG Chatbot Agent with OpenAI SDK. The specification includes:

- User scenarios for answering book questions via API, validating retrieval-based answers, and accessing source information
- Functional requirements covering the FastAPI endpoint, OpenAI Agents SDK integration, Qdrant retrieval, answer generation, and response format
- Key entities including Question, Retrieved Chunks, Answer, and Source URLs
- Success criteria with measurable outcomes for endpoint performance, agent creation, retrieval accuracy, hallucination prevention, and local execution

The specification follows the template structure and has been validated against quality criteria with a checklist confirming completeness.

## Outcome

- ✅ Impact: Created complete feature specification for RAG chatbot agent with measurable success criteria
- 🧪 Tests: none
- 📁 Files: Created spec.md and requirements checklist
- 🔁 Next prompts: Ready for planning phase with /sp.plan
- 🧠 Reflection: Specification addresses all core requirements for OpenAI agent-based RAG system with proper validation criteria

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): none
- Next experiment (smallest change to try): Proceed to planning phase