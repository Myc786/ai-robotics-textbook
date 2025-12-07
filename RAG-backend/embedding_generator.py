# RAG-backend/embedding_generator.py

import os
from typing import List, Dict
import re

# Placeholder for an embedding client (e.g., OpenAI, Anthropic)
# In a real scenario, you'd initialize your chosen embedding model here.
class EmbeddingClient:
    def __init__(self):
        self.api_key = os.getenv("EMBEDDING_API_KEY")
        if not self.api_key:
            print("Warning: EMBEDDING_API_KEY not set. Embedding generation will use dummy vectors.")

    def generate_embedding(self, text: str) -> List[float]:
        # Placeholder for actual embedding API call
        # For demonstration, returning a dummy vector
        # Replace with actual API call to OpenAI, Anthropic, etc.
        if self.api_key: # Simulate API call if key is present
            print(f"Generating real-ish embedding for: {text[:50]}...")
            # Example using a common embedding size (e.g., for OpenAI ada-002)
            return [0.1] * 1536 # Dummy vector
        else:
            print(f"Generating dummy embedding for: {text[:50]}...")
            return [0.0] * 1536 # Dummy vector

def chunk_text(text: str, max_chunk_size: int = 500) -> List[str]:
    """
    Simple text chunking function by paragraphs.
    For more advanced chunking, consider libraries like Langchain's RecursiveCharacterTextSplitter.
    """
    paragraphs = re.split(r'\n\s*\n', text) # Split by double newline
    chunks = []
    current_chunk = ""
    for para in paragraphs:
        if len(current_chunk) + len(para) + 2 <= max_chunk_size:
            current_chunk += (para + "\n\n")
        else:
            if current_chunk:
                chunks.append(current_chunk.strip())
            current_chunk = para + "\n\n"
    if current_chunk:
        chunks.append(current_chunk.strip())
    return chunks

def generate_embeddings_for_file(file_path: str) -> List[Dict]:
    embedding_client = EmbeddingClient()
    embeddings_data = []

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        chunks = chunk_text(content)
        for i, chunk in enumerate(chunks):
            embedding = embedding_client.generate_embedding(chunk)
            embeddings_data.append({
                "chunk_id": f"{os.path.basename(file_path).replace('.md', '')}_chunk_{i}",
                "content": chunk,
                "embedding": embedding,
                "file_path": file_path
            })
    except Exception as e:
        print(f"Error processing file {file_path}: {e}")

    return embeddings_data

if __name__ == "__main__":
    # Example usage: Replace with actual path to a markdown file
    example_file = "../docs/1-introduction-to-physical-ai.md"
    if os.path.exists(example_file):
        print(f"Processing embeddings for {example_file}")
        data = generate_embeddings_for_file(example_file)
        for entry in data:
            print(f"Chunk ID: {entry['chunk_id']}, Content (first 50 chars): {entry['content'][:50]}...")
            print(f"Embedding length: {len(entry['embedding'])}")
    else:
        print(f"Example file '{example_file}' not found. Please create it or update the path.")
