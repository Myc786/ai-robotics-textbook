import pytest
from fastapi.testclient import TestClient
from src.main import app
from unittest.mock import patch, AsyncMock
from src.models.document import RetrievedChunk


def test_health_check():
    """Test the health check endpoint."""
    client = TestClient(app)
    response = client.get("/health")

    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert data["status"] == "healthy"


@pytest.mark.asyncio
@patch('src.services.rag_agent_service.rag_agent_service')
def test_chat_endpoint(mock_rag_agent_service):
    """Test the chat endpoint."""
    client = TestClient(app)

    # Mock the RAG agent service response
    mock_response = AsyncMock()
    mock_response.query = "Test query"
    mock_response.response = "Test response"
    mock_response.retrieved_chunks = [
        RetrievedChunk(
            chunk_id="test_chunk_1",
            content="Test content",
            score=0.8
        )
    ]
    mock_response.response_status = "success"

    mock_rag_agent_service.process_query = AsyncMock(return_value=mock_response)

    # Send request
    payload = {
        "query": "Test query",
        "top_k": 3,
        "similarity_threshold": 0.5
    }

    response = client.post("/api/v1/chat", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert data["query"] == "Test query"
    assert data["response"] == "Test response"
    assert len(data["retrieved_chunks"]) == 1
    assert data["response_status"] == "success"


@patch('src.services.document_service.document_service')
def test_upload_document_endpoint(mock_document_service):
    """Test the document upload endpoint."""
    client = TestClient(app)

    # Mock the document service
    mock_document_service.process_and_store_document = AsyncMock(return_value="test_doc_id")

    # Send request
    payload = {
        "title": "Test Document",
        "content": "This is a test document content.",
    }

    response = client.post("/api/v1/documents", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert data["document_id"] == "test_doc_id"
    assert data["status"] == "indexed"


def test_invalid_query():
    """Test the chat endpoint with invalid data."""
    client = TestClient(app)

    # Send request with missing required field
    payload = {
        # Missing query field
        "top_k": 3,
        "similarity_threshold": 0.5
    }

    response = client.post("/api/v1/chat", json=payload)

    # Should return 422 for validation error
    assert response.status_code == 422