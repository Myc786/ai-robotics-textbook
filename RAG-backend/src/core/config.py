from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional
import os


class Settings(BaseSettings):
    # Environment
    environment: str = "development"
    log_level: str = "INFO"

    # API Keys and URLs
    cohere_api_key: str = os.getenv("COHERE_API_KEY", "")
    openai_api_key: Optional[str] = os.getenv("OPENAI_API_KEY")
    google_api_key: Optional[str] = os.getenv("GOOGLE_API_KEY")
    qdrant_url: str = os.getenv("QDRANT_URL", "")
    qdrant_api_key: Optional[str] = os.getenv("QDRANT_API_KEY")

    # Database (optional)
    database_url: Optional[str] = os.getenv("DATABASE_URL")

    # Application
    embedding_model: str = "multilingual-light-v2.0"
    default_top_k: int = 5
    default_similarity_threshold: float = 0.5
    max_chunk_size: int = 1000
    chunk_overlap: int = 100

    # CORS
    allowed_origins: list[str] = ["*"]  # In production, specify your frontend URL

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding='utf-8',
        case_sensitive=False
    )

    def check_required_fields(self):
        """Check if required fields are set (non-empty) and raise an error if not."""
        if not self.cohere_api_key and self.environment != "testing":
            raise ValueError("COHERE_API_KEY is required but not set")
        if not self.qdrant_url and self.environment != "testing":
            raise ValueError("QDRANT_URL is required but not set")
        # Database is now optional for basic functionality


# Create a single instance of settings
# We'll use lazy validation that checks the environment when needed
settings = Settings()