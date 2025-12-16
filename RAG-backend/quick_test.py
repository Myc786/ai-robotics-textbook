import sys
import os
import importlib.util
from pathlib import Path
import time

# Load modules using importlib
def load_module_from_path(module_name, file_path):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

# Load the required modules using correct paths from the RAG-Backend directory
vector_store_module = load_module_from_path('vector_store_service', 'src/services/vector_store_service.py')
embedding_module = load_module_from_path('embedding_service', 'src/services/embedding_service.py')
document_module = load_module_from_path('document', 'src/models/document.py')

from uuid import uuid4
import asyncio

async def quick_test():
    print('Starting quick test of book content indexing...')

    # Get the service instances
    vector_store_service = vector_store_module.vector_store_service
    embedding_service = embedding_module.embedding_service

    # Initialize the vector store collection
    await vector_store_service.initialize_collection()
    print(f'Connected to Qdrant collection: {vector_store_service.collection_name}')

    # Get just the first book file to test
    docs_dir = Path('../docs')
    markdown_files = list(docs_dir.glob('1-introduction-to-physical-ai.md'))  # Just first file for test

    print(f'Found {len(markdown_files)} markdown file to test')

    # Process just the first markdown file
    total_chunks = 0
    for i, file_path in enumerate(markdown_files):
        print(f'\nProcessing {file_path.name} ({i+1}/{len(markdown_files)})...')

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

            # Split content into larger chunks to reduce API calls
            max_chunk_size = 2000  # Increase chunk size to reduce number of embeddings needed
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

            print(f'  Split into {len(chunks)} chunks (reduced to minimize API calls)')

            # Process each chunk
            chunk_objects = []
            embeddings = []

            for j, chunk_content in enumerate(chunks[:2]):  # Only process first 2 chunks to stay within rate limits
                if chunk_content.strip():  # Only process non-empty chunks
                    # Create a unique chunk ID
                    chunk_id = f'{file_path.stem}_chunk_{j}_{str(uuid4())[:8]}'

                    # Create document chunk object
                    chunk_obj = document_module.DocumentChunk(
                        chunk_id=chunk_id,
                        document_id=file_path.stem,
                        content=chunk_content[:2000],  # Limit content size to avoid issues
                        url=f'/docs/{file_path.name}',
                        chapter=file_path.stem,
                        section=f'Section {j+1}',
                        page_number=j+1,
                        metadata={
                            'source_file': file_path.name,
                            'chunk_index': j,
                            'original_length': len(chunk_content)
                        }
                    )

                    chunk_objects.append(chunk_obj)

                    # Generate embedding for the chunk
                    try:
                        print(f'    Generating embedding for chunk {j+1}...')
                        embedding = await embedding_service.embed_query(chunk_content[:2000])
                        embeddings.append(embedding)
                        print(f'    ✓ Generated embedding for chunk {j+1}')

                        # Add delay to respect rate limits
                        time.sleep(2)

                    except Exception as e:
                        print(f'    Error generating embedding for chunk {j+1}: {e}')
                        continue

            # Add chunks to vector store if we have any
            if chunk_objects and embeddings:
                try:
                    await vector_store_service.upsert_document_chunks(chunk_objects, embeddings)
                    print(f'    Successfully added {len(chunk_objects)} chunks to vector store')
                    total_chunks += len(chunk_objects)
                except Exception as e:
                    print(f'    Error adding chunks to vector store: {e}')
                    import traceback
                    traceback.print_exc()

        except Exception as e:
            print(f'  Error processing {file_path.name}: {e}')
            import traceback
            traceback.print_exc()

    print(f'\nSuccessfully indexed {total_chunks} chunks from {len(markdown_files)} book file into Qdrant!')

    # Test a sample query to verify the content is searchable
    print('\nTesting search functionality...')
    try:
        test_query = 'What is Physical AI?'
        query_embedding = await embedding_service.embed_query(test_query)

        results = await vector_store_service.search(query_vector=query_embedding, top_k=3)
        print(f'Search test returned {len(results)} results')

        if results:
            print('Sample result:')
            first_result = results[0]
            print(f'  Content preview: {first_result.payload.get("content", "")[:100]}...')
            print(f'  Score: {first_result.score}')
            print(f'  Source: {first_result.payload.get("url", "Unknown")}')
        else:
            print('No results found - content may need more processing')

    except Exception as e:
        print(f'Error during search test: {e}')
        import traceback
        traceback.print_exc()

    print('\nQuick test completed. To index all books, you may need to:')
    print('1. Use a Cohere Production API key with higher rate limits')
    print('2. Or modify the system to use Google embeddings instead of Cohere')
    print('3. Or process files in smaller batches with delays')

asyncio.run(quick_test())