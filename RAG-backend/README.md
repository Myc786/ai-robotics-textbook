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
2. **Railway**: Connect your GitHub repo directly
3. **Render**: Create a new Web Service
4. **Docker**: Use the provided Dockerfile

## Environment Variables

Required environment variables for production:

```env
COHERE_API_KEY=your_cohere_api_key
QDRANT_URL=your_qdrant_url
QDRANT_API_KEY=your_qdrant_api_key
DATABASE_URL=your_postgres_database_url
```

Optional variables:
```env
ENVIRONMENT=production
LOG_LEVEL=INFO
OPENAI_API_KEY=your_openai_api_key  # Optional
ALLOWED_ORIGINS=["https://your-frontend.com"]  # For CORS
```

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