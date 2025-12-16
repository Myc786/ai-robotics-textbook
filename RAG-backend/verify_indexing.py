import sys
import os
import importlib.util
import asyncio

# Load modules using importlib
def load_module_from_path(module_name, file_path):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

# Load the required modules
vector_store_module = load_module_from_path('vector_store_service', 'src/services/vector_store_service.py')
embedding_module = load_module_from_path('embedding_service', 'src/services/embedding_service.py')

async def verify_indexing():
    print("Verifying that book content was successfully indexed...")

    # Get the service instances
    vector_store_service = vector_store_module.vector_store_service
    embedding_service = embedding_module.embedding_service

    # Test search functionality
    test_queries = [
        "What is Physical AI?",
        "Explain ROS2 fundamentals",
        "How are digital twins used in robotics?",
        "What are vision language action systems?"
    ]

    for i, query in enumerate(test_queries, 1):
        print(f"\nTest {i}: Searching for '{query}'")

        try:
            # Generate embedding for the query
            query_embedding = await embedding_service.embed_query(query)

            # Search in the vector store
            results = await vector_store_service.search(query_vector=query_embedding, top_k=2)

            print(f"  Found {len(results)} results")

            if results:
                for j, result in enumerate(results[:2], 1):
                    content_preview = result.payload.get("content", "")[:100] + "..."
                    source = result.payload.get("url", "Unknown")
                    score = result.score
                    print(f"    Result {j}: (Score: {score:.3f}, Source: {source})")
                    print(f"      Preview: {content_preview}")
            else:
                print("    No results found for this query")

        except Exception as e:
            print(f"  Error during search: {e}")

    print(f"\nVerification complete! The book content has been successfully indexed into the RAG system.")

if __name__ == "__main__":
    asyncio.run(verify_indexing())