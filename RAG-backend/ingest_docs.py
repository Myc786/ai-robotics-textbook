"""
Script to ingest textbook markdown files directly into Qdrant.
Bypasses PostgreSQL for cases where the database is unavailable.
"""
import os
import uuid
from pathlib import Path
from dotenv import load_dotenv
import cohere
from qdrant_client import QdrantClient
from qdrant_client.http import models
import tiktoken

# Load environment variables
load_dotenv()

# Initialize clients
cohere_client = cohere.Client(api_key=os.getenv("COHERE_API_KEY"))
qdrant_client = QdrantClient(
    url=os.getenv("QDRANT_URL"),
    api_key=os.getenv("QDRANT_API_KEY"),
)
COLLECTION_NAME = os.getenv("QDRANT_COLLECTION_NAME", "RAG_embeddings")

# Tokenizer for counting
tokenizer = tiktoken.get_encoding("cl100k_base")


def count_tokens(text: str) -> int:
    """Count tokens in text."""
    return len(tokenizer.encode(text))


def chunk_text(text: str, max_tokens: int = 500, overlap: int = 50) -> list:
    """Split text into chunks with overlap."""
    sentences = text.replace('\n', ' ').split('. ')
    chunks = []
    current_chunk = []
    current_tokens = 0

    for sentence in sentences:
        sentence = sentence.strip()
        if not sentence:
            continue
        sentence_tokens = count_tokens(sentence)

        if current_tokens + sentence_tokens > max_tokens and current_chunk:
            chunks.append('. '.join(current_chunk) + '.')
            # Keep last few sentences for overlap
            overlap_sentences = current_chunk[-2:] if len(current_chunk) > 2 else current_chunk[-1:]
            current_chunk = overlap_sentences
            current_tokens = sum(count_tokens(s) for s in current_chunk)

        current_chunk.append(sentence)
        current_tokens += sentence_tokens

    if current_chunk:
        chunks.append('. '.join(current_chunk) + '.')

    return chunks


def extract_title_from_markdown(content: str, filename: str) -> str:
    """Extract title from markdown content or filename."""
    lines = content.split('\n')
    for line in lines:
        if line.startswith('# '):
            return line[2:].strip()
    # Fallback to filename
    return filename.replace('.md', '').replace('-', ' ').title()


def ensure_collection_exists():
    """Create Qdrant collection if it doesn't exist."""
    collections = qdrant_client.get_collections()
    collection_names = [c.name for c in collections.collections]

    if COLLECTION_NAME not in collection_names:
        qdrant_client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=models.VectorParams(
                size=1024,  # Cohere embed-english-v3.0 dimension
                distance=models.Distance.COSINE
            )
        )
        print(f"Created collection: {COLLECTION_NAME}")
    else:
        print(f"Collection {COLLECTION_NAME} already exists")


def ingest_markdown_file(filepath: str, book_title: str = "Physical AI & Humanoid Robotics"):
    """Ingest a single markdown file into Qdrant."""
    import time
    print(f"Processing: {filepath}")

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    filename = os.path.basename(filepath)
    chapter_title = extract_title_from_markdown(content, filename)

    # Chunk the content
    chunks = chunk_text(content)
    print(f"  Created {len(chunks)} chunks")

    points = []
    for i, chunk_content in enumerate(chunks):
        if not chunk_content.strip():
            continue

        # Rate limit: wait between API calls (40 calls/min = ~1.5s between calls)
        time.sleep(1.6)

        # Generate embedding
        response = cohere_client.embed(
            texts=[chunk_content],
            model="embed-english-v3.0",
            input_type="search_document"
        )
        embedding = response.embeddings[0]

        point_id = str(uuid.uuid4())
        points.append(
            models.PointStruct(
                id=point_id,
                vector=embedding,
                payload={
                    "chunk_id": point_id,
                    "book_id": book_title,
                    "chapter_id": chapter_title,
                    "section_id": f"Chunk {i+1}",
                    "content": chunk_content,
                    "source_file": filename
                }
            )
        )

    # Batch upsert to Qdrant
    if points:
        qdrant_client.upsert(
            collection_name=COLLECTION_NAME,
            points=points
        )
        print(f"  Stored {len(points)} embeddings in Qdrant")

    return len(points)


def main():
    """Main ingestion function."""
    docs_path = Path(__file__).parent.parent / "docs"

    if not docs_path.exists():
        print(f"Docs directory not found: {docs_path}")
        return

    # Ensure collection exists
    ensure_collection_exists()

    # Get all markdown files
    md_files = list(docs_path.glob("*.md"))
    print(f"Found {len(md_files)} markdown files to ingest")

    total_chunks = 0
    for md_file in md_files:
        try:
            chunks_created = ingest_markdown_file(str(md_file))
            total_chunks += chunks_created
        except Exception as e:
            print(f"  Error processing {md_file}: {e}")

    print(f"\nIngestion complete! Total chunks created: {total_chunks}")

    # Verify collection
    collection_info = qdrant_client.get_collection(COLLECTION_NAME)
    print(f"Collection {COLLECTION_NAME} now has {collection_info.points_count} points")


if __name__ == "__main__":
    main()
