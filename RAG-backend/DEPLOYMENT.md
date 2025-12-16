# Deployment Guide for RAG Chatbot Backend

## Overview
This guide explains how to deploy the RAG Chatbot backend to production.

## Prerequisites
- Access to Cohere API
- Qdrant Cloud account (or self-hosted Qdrant instance)
- Neon Postgres account (or other PostgreSQL database)
- A server or cloud platform to host the application

## Environment Variables
Create a `.env` file with the following variables:

```env
# Environment
ENVIRONMENT=production
LOG_LEVEL=INFO

# API Keys
COHERE_API_KEY=your_cohere_api_key_here
OPENAI_API_KEY=your_openai_api_key_here  # Optional, for enhanced responses
QDRANT_URL=your_qdrant_cloud_url_here
QDRANT_API_KEY=your_qdrant_api_key_here

# Database
DATABASE_URL=postgresql://username:password@your-postgres-url/dbname

# Application
EMBEDDING_MODEL=multilingual-light-v2.0
DEFAULT_TOP_K=5
DEFAULT_SIMILARITY_THRESHOLD=0.5
MAX_CHUNK_SIZE=1000
CHUNK_OVERLAP=100

# CORS - Update this to your frontend URL in production
ALLOWED_ORIGINS=["https://your-frontend-domain.com","http://localhost:3000"]
```

## Deployment Options

### Option 1: Deploy to Heroku
1. Create a Heroku app
2. Add the Heroku Git remote
3. Set environment variables in Heroku dashboard
4. Deploy using `git push heroku main`

### Option 2: Deploy to Railway
1. Create a Railway account
2. Connect your GitHub repository
3. Railway will automatically detect the Python app
4. Add environment variables in Railway dashboard
5. Deploy automatically on push to main branch

### Option 3: Deploy to Render
1. Create a Render account
2. Create a new Web Service
3. Connect your GitHub repository
4. Set environment variables in Render dashboard
5. Render will automatically build and deploy

### Option 4: Self-hosting
1. Clone the repository to your server
2. Set up a Python virtual environment
3. Install dependencies: `pip install -r requirements.txt`
4. Set environment variables
5. Run the application: `uvicorn src.main:app --host 0.0.0.0 --port 8000`

## Database Setup
1. Run database migrations: `alembic upgrade head`
2. This will create the necessary tables in your Postgres database

## API Endpoints
- `POST /api/v1/chat` - Main chat endpoint for queries
- `POST /api/v1/documents` - Upload and index documents
- `GET /api/v1/health` - Health check endpoint

## Frontend Integration
Your frontend at https://myapp-beta-eight.vercel.app/ can connect to the backend using standard fetch/XHR requests to the backend URL.

Example integration:
```javascript
// Example of how to call the backend from your frontend
const response = await fetch('https://your-backend-url/api/v1/chat', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    query: 'Your question here',
    selected_text: 'Optional selected text for constrained search',
    top_k: 5,
    similarity_threshold: 0.5,
    search_scope: 'full_book' // or 'selected_text_only'
  })
});

const data = await response.json();
console.log(data);
```

## Monitoring
- The application logs all queries and responses
- Monitor the application logs for performance and errors
- Set up alerts for error rates and response times

## Scaling
- The application is designed to be stateless
- Can be scaled horizontally behind a load balancer
- Consider using a connection pooler for database connections at scale