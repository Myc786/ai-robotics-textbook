---
title: RAG Chatbot Backend
emoji: 🤖
colorFrom: blue
colorTo: purple
sdk: docker
pinned: false
license: mit
---

# RAG Chatbot Backend

This is the backend for a book-authoritative RAG chatbot that provides answers grounded in book content with zero hallucinations.

## Features

- **Faithful Responses**: Answers are strictly grounded in provided book content with zero hallucinations
- **Multiple Input Formats**: Supports PDF, HTML, Markdown, and MDX files
- **Web Content Ingestion**: Can ingest content from URLs and sitemaps
- **Selected Text Mode**: Users can select specific text and ask questions about only that text
- **Performance Optimized**: Includes caching and performance monitoring
- **Extensible**: Supports both Cohere and OpenRouter models

## Prerequisites

- Python 3.11+
- Pip package manager

## Setup

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Copy the environment file and add your credentials:
   ```bash
   cp .env.example .env
   ```
   Update the .env file with your actual API keys and configuration

## Configuration

The application uses the following environment variables:

- `COHERE_API_KEY`: Your Cohere API key
- `QDRANT_URL`: Your Qdrant cluster URL
- `QDRANT_API_KEY`: Your Qdrant API key
- `DATABASE_URL`: Your Neon Postgres database URL
- `OPENROUTER_API_KEY`: (Optional) Your OpenRouter API key
- `OPENROUTER_MODEL`: (Optional) OpenRouter model to use
- `OPENROUTER_BASE_URL`: (Optional) OpenRouter base URL
- `APP_ENV`: Application environment (default: development)
- `LOG_LEVEL`: Logging level (default: info)

## Running the Application

To start the server:

```bash
python start_server.py
```

Or using uvicorn directly:

```bash
uvicorn src.api.main:app --reload
```

The API will be available at `http://localhost:8000`

## API Endpoints

- `GET /` - Root endpoint
- `GET /api/v1/health` - Health check
- `POST /api/v1/chat` - Main chat endpoint
- `POST /api/v1/ingest` - Content ingestion endpoint

### Chat Endpoint Usage

```json
{
  "query_text": "Your question here",
  "mode": "global" or "selected_text",
  "selected_text": "Text selected by user (optional)"
}
```

### Ingest Endpoint Usage

```bash
curl -X POST "http://localhost:8000/api/v1/ingest" \
  -H "Content-Type: application/json" \
  -d '{
    "source": "path/to/file/or/url",
    "source_type": "pdf, html, md, mdx, url, or sitemap",
    "book_title": "Title of the book",
    "author": "Author name (optional)"
  }'
```

## Supported Ingestion Sources

The system supports ingesting content from:

- PDF files
- HTML files
- Markdown (MD) files
- MDX files
- Web pages via URL
- Multiple pages via sitemap.xml

## Architecture

The application follows a service-oriented architecture with:

- **Models**: Pydantic models for data validation
- **Services**: Business logic for ingestion, embedding, retrieval, and generation
- **API**: FastAPI endpoints
- **Config**: Settings and database connections
- **Utils**: Helper functions for text processing and logging

## Hugging Face Spaces Deployment

This backend is deployed on Hugging Face Spaces using Docker SDK.

### Required Secrets

Configure these secrets in your HF Space Settings:

- `COHERE_API_KEY`: Your Cohere API key for embeddings
- `QDRANT_URL`: Your Qdrant Cloud cluster URL
- `QDRANT_API_KEY`: Your Qdrant API key
- `QDRANT_COLLECTION_NAME`: Collection name (default: RAG_embedding)
- `OPENROUTER_API_KEY`: Your OpenRouter API key for LLM generation
- `OPENROUTER_MODEL`: Model to use (default: meta-llama/llama-3.2-3b-instruct:free)
- `OPENROUTER_BASE_URL`: OpenRouter base URL (default: https://openrouter.ai/api/v1)

### Deployment Steps

1. Create a new Space on Hugging Face with Docker SDK
2. Upload the `rag-backend/` directory contents
3. Configure secrets in Space Settings
4. The Space will automatically build and deploy