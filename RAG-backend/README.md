# RAG Chatbot for AI-Native Published Book

This is a Retrieval-Augmented Generation (RAG) chatbot that answers user questions strictly using the published book content, following zero hallucination principles.

## Architecture

The system follows a retrieval-first approach with the following components:

- **Backend**: FastAPI application
- **Embeddings**: Cohere for generating text embeddings
- **Vector Database**: Qdrant Cloud for similarity search
- **Metadata Store**: Neon Serverless Postgres for document metadata
- **Agent Framework**: OpenAI Agents SDK for response generation

## Features

- Zero hallucination: Answers only from retrieved book content
- Support for full-book and selected-text-only queries
- Context sufficiency evaluation
- Source attribution for all responses
- Document management (upload, indexing, deletion)

## Project Structure

```
backend/
├── src/
│   ├── models/          # Data models and schemas
│   ├── services/        # Business logic and service layers
│   ├── api/            # API endpoints and routes
│   ├── core/           # Configuration and core utilities
│   └── utils/          # Helper functions and utilities
├── tests/              # Test files
├── requirements.txt    # Python dependencies
└── alembic/            # Database migrations
```

## Environment Setup

1. Create a `.env` file based on `.env.example`:
```bash
cp .env.example .env
```

2. Fill in your API keys and connection details in `.env`

## Running the Application

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run database migrations:
```bash
alembic upgrade head
```

3. Start the development server:
```bash
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

The application will be available at `http://localhost:8000`

## API Endpoints

### Chat
- `POST /api/v1/chat` - Process a user query using the RAG system

### Documents
- `POST /api/v1/documents` - Upload and index a document
- `POST /api/v1/documents/file` - Upload a document file
- `GET /api/v1/documents/{id}` - Get document information
- `DELETE /api/v1/documents/{id}` - Delete a document

## Testing

Run the tests with:
```bash
TESTING=1 python -m pytest
```

## Deployment

For deployment instructions, see [DEPLOYMENT.md](DEPLOYMENT.md).

Quick deployment options:
1. **Heroku**: Use the provided Procfile
2. **Railway**: Connect your GitHub repo directly (see detailed instructions below)
3. **Render**: Connect your GitHub repo directly (see detailed instructions below)
4. **Docker**: Use the provided Dockerfile

### Railway Deployment Instructions

1. Go to [https://railway.app](https://railway.app) and sign up/in
2. Click "New Project"
3. Select "Deploy from GitHub repo"
4. Find and select the `Myc786/RAG-Chatbot` repository
5. Choose the `001-rag-book-chatbot` branch
6. Railway will automatically detect this as a Python project
7. Click "Deploy" - Railway will use the Procfile to run the application
8. After deployment, click on the "Variables" tab to add environment variables

### Render Deployment Instructions

1. Go to [https://render.com](https://render.com) and sign up/in
2. Click "New +" and select "Web Service"
3. Connect your GitHub account and select the `Myc786/RAG-Chatbot` repository
4. Choose the `001-rag-book-chatbot` branch
5. Set the runtime to "Python"
6. Set the build command to: `pip install -r requirements.txt`
7. Set the start command to: `uvicorn src.main:app --host=0.0.0.0 --port=$PORT`
8. Add the required environment variables (see below)
9. Increase the instance size to at least "Standard" (4GB RAM) for AI/ML operations
10. Click "Create Web Service"

### Required Environment Variables for Production

You'll need to set these environment variables in your Railway dashboard:

```env
COHERE_API_KEY=your_cohere_api_key
QDRANT_URL=your_qdrant_cloud_url
QDRANT_API_KEY=your_qdrant_api_key
DATABASE_URL=your_postgres_database_url
ENVIRONMENT=production
LOG_LEVEL=INFO
```

Optional variables:
```env
OPENAI_API_KEY=your_openai_api_key  # Optional
ALLOWED_ORIGINS=["https://myapp-beta-eight.vercel.app"]  # For CORS with your frontend
EMBEDDING_MODEL=multilingual-light-v2.0
DEFAULT_TOP_K=5
DEFAULT_SIMILARITY_THRESHOLD=0.5
MAX_CHUNK_SIZE=1000
CHUNK_OVERLAP=100
```

> **Note**: After deployment, your backend will be accessible at a Render URL like `https://your-project-name.onrender.com`. Update your Vercel frontend environment variables to point to this URL.

## Environment Variables

Required environment variables for production:

```env
COHERE_API_KEY=your_cohere_api_key
QDRANT_URL=your_qdrant_url
QDRANT_API_KEY=your_qdrant_api_key
DATABASE_URL=your_postgres_database_url
ENVIRONMENT=production
LOG_LEVEL=INFO
ALLOWED_ORIGINS=["https://ai-robotics-textbook.vercel.app", "https://Myc786.github.io", "http://localhost:3000"]  # For CORS with your frontend
```

Optional variables:
```env
OPENAI_API_KEY=your_openai_api_key  # Optional
EMBEDDING_MODEL=multilingual-light-v2.0
DEFAULT_TOP_K=5
DEFAULT_SIMILARITY_THRESHOLD=0.5
MAX_CHUNK_SIZE=1000
CHUNK_OVERLAP=100
```

For complete deployment instructions and troubleshooting, see [BACKEND_SETUP_GUIDE.md](BACKEND_SETUP_GUIDE.md).

## Development

This project follows a spec-driven development approach with the following phases:
1. Specification (`specs/rag-chatbot/spec.md`)
2. Planning (`specs/rag-chatbot/plan.md`)
3. Implementation (`src/`)
4. Testing (`tests/`)

## Security

- API keys are loaded from environment variables
- Input validation is performed on all endpoints
- Rate limiting should be implemented in production