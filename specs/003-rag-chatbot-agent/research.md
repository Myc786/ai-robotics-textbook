# Research: RAG Chatbot Agent with OpenAI SDK

## Decision: OpenAI Agents SDK Implementation
**Rationale**: Using OpenAI Agents SDK provides a structured way to create agents with custom tools. It allows for creating a custom retrieval tool that can interface with Qdrant and Cohere, then pass the results to the LLM with specific instructions to prevent hallucination.

**Alternatives considered**:
- OpenAI Function Calling: Lower-level approach but requires more manual management
- LangChain: More complex framework with broader capabilities than needed
- Direct OpenAI API: Requires more manual orchestration of tool usage

## Decision: FastAPI Framework
**Rationale**: FastAPI is a modern, fast web framework for building APIs with Python 3.7+ based on standard Python type hints. It provides automatic API documentation, high performance, and easy integration with the existing backend project.

**Alternatives considered**:
- Flask: More traditional but slower and less feature-rich than FastAPI
- Django: Overkill for this simple API endpoint
- Starlette: Lower-level than FastAPI, would require more manual work

## Decision: Single File Architecture
**Rationale**: For this implementation, keeping everything in main.py aligns with the requirement to have a single file. The structure will be organized with clear separation using functions and classes to maintain readability.

**Best practices**:
- Use type hints for better code documentation
- Separate concerns with functions for different components
- Use dependency injection for configuration
- Implement proper error handling

## Decision: Retrieval Tool Design
**Rationale**: The custom retrieval tool will take a query, generate embeddings using Cohere, search Qdrant for top 5 chunks, and return the results with metadata. This approach ensures the agent has access to relevant book content.

**Considerations**:
- Include proper error handling for API calls
- Format results in a way that's easy for the LLM to understand
- Include source metadata (URLs, titles) in the returned results

## Decision: Hallucination Prevention
**Rationale**: To prevent the LLM from hallucinating, the system will explicitly instruct the agent to only use the provided book excerpts. The prompt will emphasize using only the retrieved content and avoiding any external knowledge.

**Approach**:
- Clear system message to the agent about using only provided content
- Include retrieved chunks directly in the user message
- Use specific language to discourage hallucination