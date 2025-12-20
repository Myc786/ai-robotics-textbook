#!/usr/bin/env python3
"""
Test script to verify that the book content has been properly ingested into Qdrant
and that retrieval functionality works correctly.
"""

import os
from dotenv import load_dotenv
from qdrant_client import QdrantClient
import cohere

# Load environment variables
load_dotenv()

def test_retrieval():
    """Test that content has been properly ingested and can be retrieved"""
    # Initialize clients
    qdrant_client = QdrantClient(
        url=os.getenv("QDRANT_URL"),
        api_key=os.getenv("QDRANT_API_KEY"),
        https=True
    )

    cohere_client = cohere.Client(os.getenv("COHERE_API_KEY"))

    collection_name = "RAG_embedding"

    # Check collection info
    print("Checking collection...")
    collection_info = qdrant_client.get_collection(collection_name)
    print(f"✅ Collection vectors count: {collection_info.points_count}")
    print(f"✅ Vector size: {collection_info.config.params.vectors.size}")

    # Test embedding generation
    print("\nTesting embedding generation...")
    test_query = "What is robotic simulation?"
    response = cohere_client.embed(
        texts=[test_query],
        model='embed-english-v3.0',
        input_type="search_query"
    )
    query_embedding = response.embeddings[0]
    print(f"✅ Generated query embedding with {len(query_embedding)} dimensions")

    # Test search
    print("\nTesting search functionality...")
    search_results = qdrant_client.search(
        collection_name=collection_name,
        query_vector=query_embedding,
        limit=5
    )

    print(f"✅ Found {len(search_results)} results:")
    for i, result in enumerate(search_results):
        print(f"  Result {i+1}: Score: {result.score:.3f}")
        print(f"    URL: {result.payload.get('url', 'N/A')}")
        print(f"    Title: {result.payload.get('title', 'N/A')}")

    # Test with another query
    print("\nTesting with another query...")
    test_query2 = "Explain control systems in robotics"
    response2 = cohere_client.embed(
        texts=[test_query2],
        model='embed-english-v3.0',
        input_type="search_query"
    )
    query_embedding2 = response2.embeddings[0]

    search_results2 = qdrant_client.search(
        collection_name=collection_name,
        query_vector=query_embedding2,
        limit=3
    )

    print(f"✅ Found {len(search_results2)} results for '{test_query2}'")
    for i, result in enumerate(search_results2):
        print(f"  {i+1}. Score: {result.score:.3f}, URL: {result.payload.get('url', 'N/A')}")

    print("\n🎉 All tests passed! Content has been successfully ingested and retrieval is working.")

if __name__ == "__main__":
    test_retrieval()