from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    app_env: str = "development"
    log_level: str = "info"

    # Cohere settings
    cohere_api_key: str

    # Qdrant settings
    qdrant_url: str
    qdrant_api_key: str
    qdrant_collection_name: str = "RAG_embeddings"

    # Database settings (optional - app works without it)
    database_url: Optional[str] = None

    # Open Router settings
    openrouter_api_key: Optional[str] = None
    openrouter_model: Optional[str] = "mistralai/devstral-2512:free"
    openrouter_base_url: Optional[str] = "https://openrouter.ai/api/v1"

    # Application settings
    max_chunk_size: int = 600  # tokens
    min_chunk_size: int = 300  # tokens
    chunk_overlap_ratio: float = 0.15  # 15% overlap
    top_k: int = 5  # number of chunks to retrieve
    similarity_threshold: float = 0.5  # minimum similarity score

    class Config:
        env_file = ".env"


settings = Settings()