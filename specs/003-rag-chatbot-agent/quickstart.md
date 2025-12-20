# Quickstart: RAG Chatbot Agent with OpenAI SDK

## Setup

1. **Install Dependencies**
   ```bash
   uv sync
   ```

2. **Configure Environment**
   Create a `.env` file with the following variables:
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   COHERE_API_KEY=your_cohere_api_key_here
   QDRANT_URL=your_qdrant_url_here
   QDRANT_API_KEY=your_qdrant_api_key_here
   QDRANT_COLLECTION_NAME=your_collection_name_here
   ```

3. **Run the Application**
   ```bash
   uvicorn main:app --reload
   ```

## Usage

### API Endpoint
The chatbot is accessible at `http://localhost:8000/chat` via POST request.

### Example Request
```bash
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{"question": "What are the key concepts in neural networks? "}'
```

### Example Response
```json
{
  "answer": "Neural networks consist of interconnected layers of nodes that process information...",
  "sources": [
    "https://example.com/book/chapter3",
    "https://example.com/book/chapter5"
  ]
}
```

## Testing

Test the system with 5 different book questions using curl or Postman:
1. Factual questions about book content
2. Conceptual questions requiring synthesis
3. Technical questions about code examples
4. Comparative questions between different sections
5. Summary questions about key topics

## Validation

The system validates results by ensuring:
- Answers are based only on retrieved book content
- Source URLs are correctly attributed
- Response time is under 10 seconds
- No hallucination of information not in the book content