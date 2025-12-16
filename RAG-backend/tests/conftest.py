import pytest
import sys
import os
from unittest.mock import patch

# Add the src directory to the path so we can import modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

@pytest.fixture(autouse=True)
def mock_settings():
    """Mock settings to avoid validation errors during testing."""
    with patch.dict(os.environ, {
        'COHERE_API_KEY': 'test_key',
        'QDRANT_URL': 'https://test.qdrant.example',
        'DATABASE_URL': 'postgresql://test:test@localhost/testdb'
    }):
        # Clear any cached settings
        if 'src.core.config' in sys.modules:
            del sys.modules['src.core.config']

        # Import after patching environment
        from src.core.config import settings
        yield settings


@pytest.fixture
def sample_document_content():
    """Sample document content for testing."""
    return """
    This is a sample book content for testing the RAG system.
    The system should be able to retrieve relevant information based on user queries.
    This content covers various topics related to AI and machine learning.
    Chapter 1 discusses the basics of artificial intelligence.
    Chapter 2 covers machine learning fundamentals.
    Chapter 3 explores deep learning concepts.
    """


@pytest.fixture
def sample_query_request():
    """Sample query request for testing."""
    from src.models.document import QueryRequest
    return QueryRequest(
        query="What are the basics of artificial intelligence?",
        top_k=3,
        similarity_threshold=0.5
    )