import logging
import sys
from datetime import datetime
from typing import Dict, Any
from src.config.settings import settings


class LoggingConfig:
    """
    Configuration for application logging with performance monitoring.
    """
    
    @staticmethod
    def setup_logging():
        """Set up logging configuration based on settings."""
        # Create a custom logger
        logger = logging.getLogger("rag_chatbot")
        logger.setLevel(getattr(logging, settings.log_level.upper()))
        
        # Create handlers
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(getattr(logging, settings.log_level.upper()))
        
        # Create formatters and add to handlers
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        console_handler.setFormatter(formatter)
        
        # Add handlers to the logger
        if not logger.handlers:
            logger.addHandler(console_handler)
        
        return logger


# Initialize the logger
logger = LoggingConfig.setup_logging()


def log_performance(event: str, duration: float, metadata: Dict[str, Any] = None):
    """
    Log performance metrics.
    
    Args:
        event: Name of the event being logged
        duration: Duration of the event in seconds
        metadata: Additional metadata to log
    """
    if metadata is None:
        metadata = {}
    
    logger.info(f"PERFORMANCE - {event} - Duration: {duration:.4f}s - Metadata: {metadata}")


def log_query(query: str, mode: str, execution_time: float, confidence: float):
    """
    Log query details for monitoring.
    
    Args:
        query: The query text
        mode: The query mode ('global' or 'selected_text')
        execution_time: Time taken to process the query in milliseconds
        confidence: Confidence score of the response
    """
    logger.info(
        f"QUERY - Mode: {mode} - Confidence: {confidence:.2f} - "
        f"Execution Time: {execution_time}ms - Query: {query[:100]}..."
    )


def log_retrieval(chunks_retrieved: int, query: str, avg_similarity: float = None):
    """
    Log retrieval details.
    
    Args:
        chunks_retrieved: Number of chunks retrieved
        query: The query that triggered the retrieval
        avg_similarity: Average similarity score of retrieved chunks
    """
    details = f"RETRIEVAL - Chunks: {chunks_retrieved}"
    if avg_similarity is not None:
        details += f" - Avg Similarity: {avg_similarity:.2f}"
    details += f" - Query: {query[:100]}..."
    
    logger.info(details)


def log_error(error: Exception, context: str = ""):
    """
    Log error details.
    
    Args:
        error: The exception that occurred
        context: Context where the error occurred
    """
    logger.error(f"ERROR in {context} - {str(error)}", exc_info=True)


def log_refusal(query: str, mode: str):
    """
    Log when a query is refused (no relevant information found).
    
    Args:
        query: The query that was refused
        mode: The query mode ('global' or 'selected_text')
    """
    logger.info(f"REFUSAL - Mode: {mode} - Query: {query}")