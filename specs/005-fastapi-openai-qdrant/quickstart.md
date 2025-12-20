# Quickstart Guide: FastAPI Backend with OpenAI Agent and Qdrant Retrieval

**Feature**: 005-fastapi-openai-qdrant
**Created**: 2025-12-19
**Status**: Complete

## Prerequisites

- Python 3.8 or higher
- UV package manager
- Access to OpenAI API
- Access to Cohere API
- Qdrant vector database with indexed book content

## Setup Instructions

### 1. Clone and Navigate to Backend Directory
```bash
cd RAG-backend  # Navigate to existing backend folder
```

### 2. Install Dependencies
```bash
uv add fastapi uvicorn openai python-dotenv cohere qdrant-client
```

### 3. Update Environment Variables
Create or update the `.env` file with required API keys:
```env
OPENAI_API_KEY=your_openai_api_key_here
COHERE_API_KEY=your_cohere_api_key_here
QDRANT_URL=your_qdrant_url_here
QDRANT_API_KEY=your_qdrant_api_key_here
```

### 4. Create the Application
Create a `main.py` file with the FastAPI application implementation.

## Running the Application

### Local Development
```bash
uvicorn main:app --reload
```

The application will be available at `http://localhost:8000`

### Testing the Endpoint
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"question": "What are the basics of humanoid robotics?"}'
```

## API Usage

### Request Format
```json
{
  "question": "Your question about the book content here"
}
```

### Response Format
```json
{
  "answer": "The AI-generated answer based on book content",
  "sources": [
    "URL to source 1",
    "URL to source 2"
  ]
}
```

## Verification Steps

1. Start the application with `uvicorn main:app --reload`
2. Test with 5 real book questions using curl or Postman
3. Verify answers are accurate and grounded in book content
4. Confirm source URLs are correctly cited in responses
5. Check that the system only uses provided book content (no hallucination)

## Troubleshooting

- If API keys are not loading, verify the `.env` file is in the correct directory
- If Qdrant connection fails, check URL and API key configuration
- If responses seem inaccurate, verify the vector database has been properly indexed with book content