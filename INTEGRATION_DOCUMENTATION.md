# RAG Backend and Frontend Integration Documentation

## Overview
This document describes the integration between the RAG backend (FastAPI) and the frontend (Docusaurus) for the Physical AI & Humanoid Robotics textbook project.

## Completed Integration Steps

### 1. Frontend Configuration Updates
- Updated the Chatbot component to use environment variables for backend URL configuration
- Changed from hardcoded URLs to using `NEXT_PUBLIC_RAG_BACKEND_URL` environment variable
- Updated setup instructions to reflect proper configuration

### 2. Backend Configuration Updates
- Updated .env file with proper credentials:
  - Cohere API Key: Successfully configured
  - Qdrant URL: Updated to include port 6333
  - Qdrant API Key: Configured with access to "Hackathon-Giaic" collection
  - Google API Key: Added for Gemini integration
  - Database URL: Updated to remove problematic parameters

### 3. API Integration
- Integrated Google Gemini API as the primary LLM service
- Updated RAG agent service to use Gemini for response generation
- Maintained fallback to simulated responses if API is unavailable
- Fixed collection name in vector store to match Qdrant access permissions

### 4. Environment Setup
- Created proper .env files for both frontend and backend
- Configured CORS settings for proper cross-origin communication
- Set up proper database connection strings (asyncpg format)

## Current System Status

### Working Components
- ✅ Backend server successfully starts and runs on port 8000
- ✅ Health endpoint is accessible: `GET /health`
- ✅ Google Generative AI configured successfully
- ✅ Qdrant vector store connection established
- ✅ Frontend can connect to backend via environment variables
- ✅ Database dependency removed (optional now)

### Known Issues
- ⚠️ Chat functionality not working due to empty vector store (no documents indexed)
- ⚠️ Document upload endpoints may still have issues due to missing database functionality

## How to Use the Integrated System

### 1. Starting the Services
```bash
# Terminal 1: Start backend
cd RAG-Backend
python -m uvicorn src.main:app --host 0.0.0.0 --port 8000

# Terminal 2: Start frontend (in project root)
npm start
```

### 2. Frontend Configuration
The frontend automatically uses the backend URL from the environment variable:
- Default: `NEXT_PUBLIC_RAG_BACKEND_URL=http://localhost:8000`
- Update in `.env` file if backend is hosted elsewhere

### 3. Backend Configuration
Ensure the `.env` file in RAG-Backend contains:
```
COHERE_API_KEY=your_cohere_api_key
QDRANT_URL=https://your-qdrant-url:6333
QDRANT_API_KEY=your_qdrant_api_key
GOOGLE_API_KEY=your_google_api_key
DATABASE_URL=postgresql+asyncpg://...
```

## API Endpoints

### Backend Endpoints
- `GET /health` - Health check
- `POST /api/v1/chat` - Chat query processing
- `POST /api/v1/documents` - Document upload
- `POST /api/v1/documents/file` - File upload

### Frontend Integration
- Chat interface at `/rag-chat` page
- Uses the Chatbot component with environment-based backend configuration

## Troubleshooting

### Common Issues
1. **Database Connection Error**: "connect() got an unexpected keyword argument 'sslmode'"
   - Solution: Verify DATABASE_URL format for asyncpg compatibility

2. **Qdrant Access Error**: "Forbidden: Access to collection required"
   - Solution: Ensure collection name matches API key permissions

3. **CORS Issues**: Requests blocked due to cross-origin restrictions
   - Solution: Check ALLOWED_ORIGINS in backend settings

## Next Steps

To fully operationalize the system:
1. Fix database connection issues with Neon Postgres
2. Index textbook content into the vector store
3. Test end-to-end chat functionality with real content
4. Deploy backend to a cloud service for production use
5. Update frontend to point to production backend URL

## Security Considerations

- API keys are loaded from environment variables, not hardcoded
- Vector store access is controlled through API keys
- CORS settings should be restricted in production
- Database credentials are not exposed in frontend

## Architecture Summary

- **Frontend**: Docusaurus-based with React components
- **Backend**: FastAPI with async support
- **Vector Store**: Qdrant Cloud with Cohere embeddings
- **LLM**: Google Gemini API for response generation
- **Database**: PostgreSQL for metadata (currently having connection issues)