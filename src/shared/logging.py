from .environment import ensure_environment_initialized

ensure_environment_initialized()

import logging
import os


def configure_root_logger():
    """
    Configures the root logger with application-wide settings.
    All other loggers will inherit from these settings.
    """
    # Get log level from environment variable, default to INFO if not set
    log_level_name = os.environ.get("LOG_LEVEL", "INFO").upper()
    log_level = getattr(logging, log_level_name, logging.INFO)

    # Only configure if it hasn't been configured already
    if not logging.getLogger().handlers:
        # Configure the root logger
        logging.basicConfig(
            level=log_level,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        )

        logging.debug(f"Root logger initialized with level: {log_level_name}")


_app_logger = None


def get_app_logger():
    """
    Returns the application logger, initializing the root logger if needed.
    """
    global _app_logger

    if _app_logger is None:
        # Configure the root logger first
        configure_root_logger()

        # Create the application logger
        _app_logger = logging.getLogger("_app_")

    return _app_logger
