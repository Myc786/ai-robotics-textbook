import asyncio
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'RAG-Backend', 'src'))

from uuid import uuid4
from core.config import settings
from services.vector_store_service import vector_store_service
from services.embedding_service import embedding_service
from models.document import DocumentChunk

async def add_test_content():
    print("Adding test content to vector store...")

    # Initialize the collection
    await vector_store_service.initialize_collection()

    # Test content about Physical AI
    test_contents = [
        "Physical AI is an interdisciplinary field combining robotics, artificial intelligence, and control theory to create intelligent systems that can interact with the physical world.",
        "Humanoid robotics focuses on creating robots with human-like form and behavior, enabling natural interaction with human environments.",
        "ROS2 (Robot Operating System 2) provides a flexible framework for writing robot software, including hardware abstraction, device drivers, and message passing.",
        "Digital twin simulation creates virtual replicas of physical systems for testing, optimization, and control in robotics applications.",
        "Vision-Language-Action systems integrate perception, understanding, and motor control to enable robots to perform complex tasks based on visual and linguistic input."
    ]

    # Create document chunks
    chunks = []
    embeddings = []

    for i, content in enumerate(test_contents):
        chunk_id = f"test_chunk_{i}_{str(uuid4())[:8]}"
        chunk = DocumentChunk(
            chunk_id=chunk_id,
            document_id="test_document",
            content=content,
            url="/test-content",
            chapter="Introduction",
            section=f"Section {i+1}",
            page_number=i+1,
            metadata={"source": "test_content", "index": i}
        )
        chunks.append(chunk)

        # Generate embedding for the content
        embedding = await embedding_service.embed_query(content)
        embeddings.append(embedding)
        print(f"Generated embedding for chunk {i+1}")

    # Upsert to vector store
    try:
        await vector_store_service.upsert_document_chunks(chunks, embeddings)
        print(f"Successfully added {len(chunks)} chunks to vector store!")

        # Test a search to verify
        test_query = "What is Physical AI?"
        query_embedding = await embedding_service.embed_query(test_query)

        results = await vector_store_service.search(query_vector=query_embedding, top_k=3)
        print(f"Search test returned {len(results)} results")
        if results:
            print("Sample result content:", results[0].payload.get('content', '')[:100] + "...")

    except Exception as e:
        print(f"Error adding content: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(add_test_content())