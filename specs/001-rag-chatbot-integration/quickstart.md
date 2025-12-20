# Quickstart Guide: RAG Chatbot Integration

**Feature**: RAG Chatbot Integration
**Created**: 2025-12-17

## Prerequisites

- Python 3.9 or higher
- UV package manager
- Access to Cohere API (API key)
- Access to Qdrant vector database (local or cloud)

## Setup

### 1. Clone or Create Project Directory

```bash
mkdir rag-backend
cd rag-backend
```

### 2. Initialize Project with UV

```bash
# Install UV if not already installed
pip install uv

# Initialize the project
uv init
```

### 3. Install Dependencies

```bash
# Add required dependencies
uv add cohere qdrant-client requests beautifulsoup4 python-dotenv
```

### 4. Set Up Environment Variables

Create a `.env` file in your project root:

```env
COHERE_API_KEY=your-cohere-api-key
QDRANT_URL=your-qdrant-url  # Optional, defaults to localhost:6333
QDRANT_API_KEY=your-qdrant-api-key  # Optional for cloud instances
```

## Basic Usage

### 1. Create the main.py file

Create a `main.py` file with the RAG implementation (the complete implementation will be provided in the development phase).

### 2. Run Indexing Process

```bash
# Index the AI Robotics textbook
python main.py index --target-url "https://ai-robotics-textbook.vercel.app/"

# Index with custom parameters
python main.py index --target-url "https://ai-robotics-textbook.vercel.app/" --chunk-size 1500 --overlap 300
```

### 3. Check Status

```bash
# Check the status of your vector database and connections
python main.py status
```

## Configuration Options

### Command Line Arguments

- `--urls`: List of URLs to index (required)
- `--chunk-size`: Size of text chunks (default: 1000 characters)
- `--overlap`: Overlap between chunks (default: 200 characters)
- `--collection`: Qdrant collection name (default: "book_embeddings")
- `--batch-size`: Number of chunks to process at once (default: 10)

### Environment Variables

- `COHERE_API_KEY`: Your Cohere API key (required)
- `QDRANT_URL`: URL of your Qdrant instance (optional)
- `QDRANT_API_KEY`: API key for Qdrant cloud (optional)
- `COHERE_MODEL`: Embedding model to use (default: "embed-multilingual-v2.0")

## Example Implementation

Here's a basic example of how to use the core functions:

```python
import os
from main import fetch_content, chunk_text, generate_embeddings, store_embeddings

# Fetch content from a URL
result = fetch_content("https://example-book.com/chapter1")
if result["success"]:
    content = result["content"]
    title = result["title"]
    url = result["metadata"]["url"]

    # Chunk the content
    chunks_result = chunk_text(content, max_chunk_size=1000, overlap=200)
    chunks = chunks_result["chunks"]

    # Generate embeddings
    embeddings_result = generate_embeddings(chunks)
    if embeddings_result["success"]:
        embeddings = embeddings_result["embeddings"]

        # Prepare entries for storage
        entries = []
        for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
            entries.append({
                "id": f"{url}_chunk_{i}",
                "vector": embedding,
                "payload": {
                    "url": url,
                    "title": title,
                    "content": chunk,
                    "content_id": url,
                    "chunk_index": i,
                    "source_type": "webpage"
                }
            })

        # Store embeddings in vector database
        store_result = store_embeddings(entries)
        if store_result["success"]:
            print(f"Successfully stored {store_result['stored_count']} embeddings")
```

## Troubleshooting

### Common Issues

1. **API Key Errors**:
   - Verify your Cohere and Qdrant API keys are correct
   - Check that environment variables are properly set

2. **Network Issues**:
   - Ensure the URLs you're trying to index are accessible
   - Check your internet connection

3. **Rate Limiting**:
   - If you encounter rate limit errors, reduce the batch size
   - Add delays between API calls if needed

### Verification Steps

1. Test API connectivity:
   ```bash
   python main.py status
   ```

2. Verify environment variables:
   ```python
   import os
   print("COHERE_API_KEY set:", bool(os.getenv("COHERE_API_KEY")))
   print("QDRANT_URL:", os.getenv("QDRANT_URL", "localhost:6333"))
   ```

## Next Steps

1. Implement the complete RAG pipeline in main.py
2. Add error handling and retry logic
3. Create unit tests for each function
4. Set up monitoring and logging
5. Deploy to your preferred environment