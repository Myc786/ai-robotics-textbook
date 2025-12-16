import sys
import os
import importlib.util

# Load modules using importlib
def load_module_from_path(module_name, file_path):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

# Load the embedding module
embedding_module = load_module_from_path('embedding_service', 'src/services/embedding_service.py')

import asyncio

async def test_embedding():
    print('Testing embedding dimensions...')

    embedding_service = embedding_module.embedding_service

    # Test embedding
    test_text = "This is a test sentence for embedding."

    try:
        embedding = await embedding_service.embed_query(test_text)
        print(f"Embedding generated successfully!")
        print(f"Embedding length: {len(embedding)}")
        print(f"First 5 values: {embedding[:5]}")
    except Exception as e:
        print(f"Error generating embedding: {e}")

asyncio.run(test_embedding())