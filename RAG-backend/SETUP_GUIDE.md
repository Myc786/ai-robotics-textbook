# RAG Backend Setup Guide

## Environment Configuration

To properly configure the RAG backend, you need to set up the following environment variables in your `.env` file:

```env
# RAG Backend Configuration
COHERE_API_KEY=your_cohere_api_key_here
QDRANT_URL=your_qdrant_cluster_url_here
QDRANT_API_KEY=your_qdrant_api_key_here
TARGET_URL=https://ai-robotics-textbook.vercel.app

# Optional configuration
CHUNK_SIZE=1000
OVERLAP=200
COLLECTION_NAME=RAG_embedding
MAX_RETRIES=3
INITIAL_BACKOFF=1.0
BACKOFF_MULTIPLIER=2.0
```

## Qdrant Configuration Requirements

The Qdrant API key must have read-write permissions for the collection specified in `COLLECTION_NAME`.

If using an existing Qdrant cloud instance, ensure your API key has the proper permissions:
- Collection: `RAG_embedding` (or your chosen collection name)
- Access: Read and Write permissions

## API Endpoint

The backend provides the following API endpoints:
- `POST /api/v1/chat` - Main chat endpoint for RAG queries
- `GET /health` - Health check endpoint

## Frontend Integration

The frontend expects to connect to the backend at the configured endpoint. Update your Docusaurus configuration with:

```js
customFields: {
  NEXT_PUBLIC_RAG_BACKEND_URL: process.env.NEXT_PUBLIC_RAG_BACKEND_URL || 'https://muhammadyounis-chatbot.hf.space',
},
```

## Running the Application

1. Start the backend server:
   ```bash
   cd rag-backend
   python -m uvicorn server:app --host 0.0.0.0 --port 8000
   ```

2. Index the content:
   ```bash
   python main.py index --target-url https://ai-robotics-textbook.vercel.app
   ```

## Troubleshooting

### Qdrant Connection Issues
- Error: `403 Forbidden` - Check that your API key has proper permissions for the specified collection
- Error: `getaddrinfo failed` - Verify that your QDRANT_URL is correct and accessible

### Frontend Connection Issues
- Ensure the backend server is running before testing the frontend
- Check CORS configuration if hosting frontend and backend on different domains