# RAG Backend for Physical AI & Humanoid Robotics Textbook

This is a FastAPI-based RAG (Retrieval-Augmented Generation) backend that enables Q&A functionality for the Physical AI & Humanoid Robotics textbook.

## Features

- Semantic search through textbook content
- Context-aware responses based on textbook chapters
- Source attribution for all answers
- Special handling for specific AI/Robotics topics

## Prerequisites

- Python 3.8+
- pip (Python package manager)

## Installation

1. Navigate to the RAG-backend directory:
   ```bash
   cd RAG-backend
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Server

1. Start the RAG server:
   ```bash
   python main.py
   ```

2. The server will start at: `http://localhost:8000`

3. Verify the server is running by visiting: `http://localhost:8000/health`

## API Endpoints

- `POST /api/v1/query` - Query the RAG system
- `GET /health` - Health check endpoint

### Query Example

```json
{
  "query": "What is Physical AI?"
}
```

Response:
```json
{
  "answer": "Physical AI refers to intelligent systems that interact with the physical world through sensors and actuators...",
  "sources": [
    {
      "title": "Introduction to Physical AI",
      "url": "/docs/introduction-to-physical-ai"
    }
  ]
}
```

## Development

During development, ensure both the backend and frontend are running:

1. Start the RAG backend server:
   ```bash
   python main.py
   ```

2. In a separate terminal, start the Docusaurus frontend:
   ```bash
   npm start
   ```

The frontend will be available at `http://localhost:3000` and will communicate with the backend at `http://localhost:8000`.

## Production Deployment

For production deployment, you'll need to:

1. Deploy the RAG backend to a cloud service (e.g., Heroku, Render, AWS, etc.)
2. Update the backend URL in the frontend components to point to your deployed backend
3. Ensure CORS settings allow requests from your frontend domain
4. Configure your frontend to use the production backend URL

## Configuration Notes

- The backend automatically reads and indexes all `.md` files in the `../docs` directory
- Document URLs are generated based on the Docusaurus documentation structure
- The search algorithm uses keyword matching with boost factors for relevant terms