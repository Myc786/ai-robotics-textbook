from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # Environment
    environment: str = "testing"
    log_level: str = "INFO"

    # API Keys and URLs
    cohere_api_key: str = "test_key"
    openai_api_key: Optional[str] = "test_openai_key"
    qdrant_url: str = "https://test.qdrant.example"
    qdrant_api_key: Optional[str] = "test_qdrant_key"

    # Database
    database_url: str = "postgresql://test:test@localhost/testdb"

    # Application
    embedding_model: str = "multilingual-light-v2.0"
    default_top_k: int = 5
    default_similarity_threshold: float = 0.5
    max_chunk_size: int = 1000
    chunk_overlap: int = 100

    class Config:
        env_file = ".env"
        case_sensitive = True


# Create a single instance of settings
settings = Settings()