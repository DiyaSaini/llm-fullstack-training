"""
Logging configuration for the application.

Call `setup_logging()` once at startup (in main.py).
Then use `get_logger(__name__)` in every module.
"""

import logging
import sys

from app.config import settings


def setup_logging() -> None:
    """
    Configure root logger based on LOG_LEVEL from settings.
    Outputs structured, human-readable logs to stdout.
    """
    log_level = getattr(logging, settings.log_level.upper(), logging.INFO)

    logging.basicConfig(
        level=log_level,
        format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        stream=sys.stdout,
    )

    # Suppress noisy third-party loggers
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)


def get_logger(name: str) -> logging.Logger:
    """
    Return a named logger.

    Usage:
        from app.logging import get_logger
        logger = get_logger(__name__)
        logger.info("Something happened")
    """
    return logging.getLogger(name)
