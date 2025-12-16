import asyncio
import os
import sys
from pathlib import Path
from uuid import uuid4

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Import the required modules from the backend
from src.services.vector_store_service import vector_store_service
from src.services.embedding_service import embedding_service
from src.models.document import DocumentChunk

async def index_book_content():
    print("Starting to index book content into Qdrant...")

    # Initialize the vector store collection
    await vector_store_service.initialize_collection()
    print(f"Connected to Qdrant collection: {vector_store_service.collection_name}")

    # Get the docs directory from the parent directory
    docs_dir = Path("../docs")
    markdown_files = list(docs_dir.glob("*.md"))

    print(f"Found {len(markdown_files)} markdown files to process")

    # Process each markdown file
    total_chunks = 0
    for i, file_path in enumerate(markdown_files):
        print(f"\nProcessing {file_path.name} ({i+1}/{len(markdown_files)})...")

        try:
            # Read the content of the markdown file
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Clean up the content - remove markdown headers and metadata if any
            lines = content.split('\n')
            clean_lines = []
            in_metadata = False

            for line in lines:
                if line.strip().startswith('---'):
                    in_metadata = not in_metadata
                    continue
                if not in_metadata:
                    clean_lines.append(line)

            clean_content = '\n'.join(clean_lines)

            # Split content into chunks (to avoid hitting token limits)
            # Simple chunking: split by paragraphs or by max length
            max_chunk_size = 1000  # characters
            chunks = []
            current_chunk = ""

            for paragraph in clean_content.split('\n\n'):
                if len(current_chunk + paragraph) < max_chunk_size:
                    current_chunk += paragraph + "\n\n"
                else:
                    if current_chunk.strip():
                        chunks.append(current_chunk.strip())
                    current_chunk = paragraph + "\n\n"

            if current_chunk.strip():
                chunks.append(current_chunk.strip())

            print(f"  Split into {len(chunks)} chunks")

            # Process each chunk
            chunk_objects = []
            embeddings = []

            for j, chunk_content in enumerate(chunks):
                if chunk_content.strip():  # Only process non-empty chunks
                    # Create a unique chunk ID
                    chunk_id = f"{file_path.stem}_chunk_{j}_{str(uuid4())[:8]}"

                    # Create document chunk object
                    chunk_obj = DocumentChunk(
                        chunk_id=chunk_id,
                        document_id=file_path.stem,
                        content=chunk_content[:2000],  # Limit content size to avoid issues
                        url=f"/docs/{file_path.name}",
                        chapter=file_path.stem,
                        section=f"Section {j+1}",
                        page_number=j+1,
                        metadata={
                            "source_file": file_path.name,
                            "chunk_index": j,
                            "original_length": len(chunk_content)
                        }
                    )

                    chunk_objects.append(chunk_obj)

                    # Generate embedding for the chunk
                    try:
                        embedding = await embedding_service.embed_query(chunk_content[:2000])
                        embeddings.append(embedding)
                        print(f"    Generated embedding for chunk {j+1}")
                    except Exception as e:
                        print(f"    Error generating embedding for chunk {j+1}: {e}")
                        continue

            # Add chunks to vector store if we have any
            if chunk_objects and embeddings:
                try:
                    await vector_store_service.upsert_document_chunks(chunk_objects, embeddings)
                    print(f"    Successfully added {len(chunk_objects)} chunks to vector store")
                    total_chunks += len(chunk_objects)
                except Exception as e:
                    print(f"    Error adding chunks to vector store: {e}")
                    import traceback
                    traceback.print_exc()

        except Exception as e:
            print(f"  Error processing {file_path.name}: {e}")
            import traceback
            traceback.print_exc()

    print(f"\nSuccessfully indexed {total_chunks} chunks from {len(markdown_files)} book files into Qdrant!")

    # Test a sample query to verify the content is searchable
    print("\nTesting search functionality...")
    try:
        test_query = "What is Physical AI?"
        query_embedding = await embedding_service.embed_query(test_query)

        results = await vector_store_service.search(query_vector=query_embedding, top_k=3)
        print(f"Search test returned {len(results)} results")

        if results:
            print("Sample result:")
            first_result = results[0]
            print(f"  Content preview: {first_result.payload.get('content', '')[:100]}...")
            print(f"  Score: {first_result.score}")
            print(f"  Source: {first_result.payload.get('url', 'Unknown')}")
        else:
            print("No results found - content may need more processing")

    except Exception as e:
        print(f"Error during search test: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(index_book_content())