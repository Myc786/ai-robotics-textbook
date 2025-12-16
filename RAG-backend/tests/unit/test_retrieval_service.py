import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from src.services.retrieval_service import RetrievalService
from src.models.document import QueryRequest


@pytest.mark.asyncio
async def test_retrieve_relevant_chunks():
    """Test the retrieve_relevant_chunks method of RetrievalService."""
    with patch('src.services.retrieval_service.embedding_service') as mock_embedding_service, \
         patch('src.services.retrieval_service.vector_store_service') as mock_vector_store_service:

        # Mock embedding service
        mock_embedding_service.embed_query = AsyncMock(return_value=[0.1, 0.2, 0.3])

        # Mock vector store service
        mock_scored_point = MagicMock()
        mock_scored_point.score = 0.8
        mock_scored_point.payload = {
            "chunk_id": "test_chunk_1",
            "content": "Test content",
            "url": "http://example.com",
            "chapter": "Chapter 1",
            "section": "Section 1",
            "page_number": 1,
            "metadata": {}
        }
        mock_vector_store_service.search = AsyncMock(return_value=[mock_scored_point])

        # Create service instance
        service = RetrievalService()

        # Test the method
        result = await service.retrieve_relevant_chunks(
            query="Test query",
            top_k=5,
            similarity_threshold=0.5
        )

        # Assertions
        assert len(result) == 1
        assert result[0].chunk_id == "test_chunk_1"
        assert result[0].content == "Test content"
        assert result[0].score == 0.8

        # Verify the services were called
        mock_embedding_service.embed_query.assert_called_once_with("Test query")
        mock_vector_store_service.search.assert_called_once()


@pytest.mark.asyncio
async def test_evaluate_context_sufficiency():
    """Test the evaluate_context_sufficiency method of RetrievalService."""
    from src.models.document import RetrievedChunk

    # Create service instance
    service = RetrievalService()

    # Create test chunks
    chunk1 = RetrievedChunk(
        chunk_id="chunk1",
        content="Test content 1",
        score=0.8
    )
    chunk2 = RetrievedChunk(
        chunk_id="chunk2",
        content="Test content 2",
        score=0.6
    )

    # Test with sufficient context
    result = await service.evaluate_context_sufficiency(
        query="Test query",
        retrieved_chunks=[chunk1, chunk2],
        minimum_chunks=1,
        minimum_similarity=0.5
    )
    assert result is True

    # Test with insufficient chunks
    result = await service.evaluate_context_sufficiency(
        query="Test query",
        retrieved_chunks=[],
        minimum_chunks=1,
        minimum_similarity=0.5
    )
    assert result is False

    # Test with insufficient similarity
    low_score_chunk = RetrievedChunk(
        chunk_id="chunk3",
        content="Test content 3",
        score=0.2  # Below threshold
    )
    result = await service.evaluate_context_sufficiency(
        query="Test query",
        retrieved_chunks=[low_score_chunk],
        minimum_chunks=1,
        minimum_similarity=0.5
    )
    assert result is False


@pytest.mark.asyncio
async def test_process_query():
    """Test the process_query method of RAGAgentService."""
    with patch('src.services.retrieval_service.retrieval_service') as mock_retrieval_service:
        from src.services.rag_agent_service import RAGAgentService
        from src.models.document import RetrievedChunk, QueryResponse, QueryRequest

        # Create an instance of the agent service for testing
        agent_service = RAGAgentService()

        # Mock the retrieval service
        mock_chunk = RetrievedChunk(
            chunk_id="test_chunk",
            content="Test content",
            score=0.8
        )
        mock_retrieval_service.retrieve_relevant_chunks = AsyncMock(return_value=[mock_chunk])
        mock_retrieval_service.evaluate_context_sufficiency = AsyncMock(return_value=True)

        # Mock the agent service's generate_response method
        with patch.object(agent_service, 'generate_response', new=AsyncMock(return_value="Test response")):
            # Create query request
            query_request = QueryRequest(query="Test query")

            # Test the method
            result = await agent_service.process_query(query_request)

            # Assertions
            assert isinstance(result, QueryResponse)
            assert result.query == "Test query"
            assert result.response == "Test response"
            assert len(result.retrieved_chunks) == 1
            assert result.retrieved_chunks[0].chunk_id == "test_chunk"
            assert result.response_status == "success"