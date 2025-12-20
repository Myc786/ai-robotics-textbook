# Quickstart: RAG Book Content Retrieval

## Setup

1. **Install Dependencies**
   ```bash
   uv sync
   ```

2. **Configure Environment**
   Create a `.env` file with the following variables:
   ```env
   COHERE_API_KEY=your_cohere_api_key_here
   QDRANT_URL=your_qdrant_url_here
   QDRANT_API_KEY=your_qdrant_api_key_here
   QDRANT_COLLECTION_NAME=your_collection_name_here
   ```

3. **Run the Retrieval Script**
   ```bash
   python test_retrieval.py
   ```

## Usage

The retrieval script can be run in two modes:

### Interactive Mode
```bash
python test_retrieval.py
```
This will start an interactive session where you can enter queries and see the results.

### Test Mode
The script will automatically run 10+ diverse test queries about book content and display the results with similarity scores.

## Example Output

```
Query: "How to implement neural networks in Python?"
Top 5 results:
1. Score: 0.892 - "Neural network implementation guide using PyTorch..."
   Source: https://example.com/book/chapter3
   Page: Neural Networks Implementation
   Chunk: 45

2. Score: 0.876 - "Python code examples for deep learning models..."
   Source: https://example.com/book/chapter5
   Page: Deep Learning Examples
   Chunk: 23
```

## Validation

The system validates results by ensuring:
- Top results have cosine similarity > 0.75
- Results contain complete text and metadata
- Response time is under 2 seconds
- Various query types (factual, conceptual, code-related) are handled