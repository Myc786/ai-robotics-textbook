# RAG Backend Configuration Guide

## Required Environment Variables for Render

To properly configure your RAG backend on Render, you need to set the following environment variables in your Render dashboard:

### 1. API Keys
- `COHERE_API_KEY`: Your Cohere API key for embeddings and language models
- `QDRANT_URL`: Your Qdrant Cloud URL (format: https://your-cluster-url.qdrant.tech:6333)
- `QDRANT_API_KEY`: Your Qdrant API key for authentication

### 2. Database Configuration
- `DATABASE_URL`: Your PostgreSQL database URL (format: postgresql://username:password@host:port/database)

### 3. Application Settings
- `ENVIRONMENT`: Set to "production"
- `LOG_LEVEL`: Set to "INFO"

### 4. CORS Configuration
- `ALLOWED_ORIGINS`: Set to your frontend domains (e.g., ["https://ai-robotics-textbook.vercel.app", "https://Myc786.github.io"])

## Data Indexing Process

Once your backend is properly configured with the environment variables, you need to index your textbook content:

### Option 1: Run Indexing Script
1. SSH into your Render instance or access the terminal
2. Run the indexing script: `python index_content.py`
3. This will index all markdown files from the docs directory into Qdrant

### Option 2: API-based Indexing
You can also use the documents API endpoint to upload and index documents:
- `POST /api/v1/documents` - Upload and index documents

## Verification Steps

1. Check health endpoint: `GET /health` should return status: "healthy"
2. Test search functionality after indexing content
3. Verify chat endpoint works: `POST /api/v1/chat`

## Common Issues and Solutions

1. **No Response from Backend**: Check that all required environment variables are set
2. **500 Errors**: Verify API keys are correct and have proper permissions
3. **No Results**: Ensure content has been indexed into the vector store
4. **CORS Errors**: Make sure ALLOWED_ORIGINS includes your frontend domains

## Frontend Configuration

Your frontend is now properly configured to connect to your Render backend at:
- `https://rag-chatbot-2ufj.onrender.com`