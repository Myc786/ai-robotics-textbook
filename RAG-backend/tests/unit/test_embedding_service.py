import pytest
from unittest.mock import AsyncMock, patch
from src.services.embedding_service import EmbeddingService


@pytest.mark.asyncio
async def test_embed_texts():
    """Test the embed_texts method of EmbeddingService."""
    # Mock the Cohere client
    with patch('src.services.embedding_service.cohere.AsyncClient') as mock_client_class:
        mock_client = AsyncMock()
        mock_client_class.return_value = mock_client

        # Mock the embed response
        mock_response = AsyncMock()
        mock_response.embeddings = [[0.1, 0.2, 0.3], [0.4, 0.5, 0.6]]
        mock_client.embed.return_value = mock_response

        # Create service instance
        service = EmbeddingService()

        # Test the method
        texts = ["Hello world", "Test embedding"]
        result = await service.embed_texts(texts)

        # Assertions
        assert len(result) == 2
        assert result[0] == [0.1, 0.2, 0.3]
        assert result[1] == [0.4, 0.5, 0.6]

        # Verify the client was called correctly
        mock_client.embed.assert_called_once_with(
            texts=texts,
            model=service.model,
            input_type="search_document"
        )


@pytest.mark.asyncio
async def test_embed_query():
    """Test the embed_query method of EmbeddingService."""
    # Mock the Cohere client
    with patch('src.services.embedding_service.cohere.AsyncClient') as mock_client_class:
        mock_client = AsyncMock()
        mock_client_class.return_value = mock_client

        # Mock the embed response
        mock_response = AsyncMock()
        mock_response.embeddings = [[0.7, 0.8, 0.9]]
        mock_client.embed.return_value = mock_response

        # Create service instance
        service = EmbeddingService()

        # Test the method
        query = "Test query"
        result = await service.embed_query(query)

        # Assertions
        assert result == [0.7, 0.8, 0.9]

        # Verify the client was called correctly
        mock_client.embed.assert_called_once_with(
            texts=[query],
            model=service.model,
            input_type="search_query"
        )


def test_service_initialization():
    """Test that the EmbeddingService initializes correctly."""
    service = EmbeddingService()

    # Just verify that the service has the expected attributes
    assert hasattr(service, 'client')
    assert hasattr(service, 'model')
    assert hasattr(service, 'logger')