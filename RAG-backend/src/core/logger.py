import logging
import sys
from .config import settings


def setup_logger(name: str = __name__) -> logging.Logger:
    """
    Set up a logger with the specified name and configured log level.
    """
    logger = logging.getLogger(name)

    # Prevent adding multiple handlers if logger already exists
    if logger.handlers:
        return logger

    # Set the log level based on settings
    logger.setLevel(getattr(logging, settings.log_level.upper()))

    # Create console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(getattr(logging, settings.log_level.upper()))

    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    console_handler.setFormatter(formatter)

    # Add handler to logger
    logger.addHandler(console_handler)

    return logger