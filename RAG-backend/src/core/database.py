from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from typing import AsyncGenerator, Optional
from .config import settings
import logging

logger = logging.getLogger(__name__)

# Initialize database engine only if database URL is provided
engine = None
AsyncSessionLocal = None

if settings.database_url:
    try:
        # Create the async database engine
        engine = create_async_engine(
            settings.database_url,
            echo=(settings.environment == "development"),  # Log SQL in development
            pool_pre_ping=True,  # Verify connections before use
            pool_recycle=300,  # Recycle connections after 5 minutes
        )

        # Create async session factory
        AsyncSessionLocal = sessionmaker(
            engine,
            class_=AsyncSession,
            expire_on_commit=False
        )
        logger.info("Database engine initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize database engine: {e}")
        engine = None
        AsyncSessionLocal = None
else:
    logger.info("Database URL not provided, database functionality will be disabled")


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency to get database session for FastAPI endpoints.
    Yields a database session if database is configured, otherwise yields None.
    """
    if AsyncSessionLocal:
        async with AsyncSessionLocal() as session:
            yield session
            await session.rollback()  # Rollback any uncommitted changes
    else:
        # Yield a dummy session-like object or None
        # For now, we'll just yield None, but endpoints should handle this case
        yield None