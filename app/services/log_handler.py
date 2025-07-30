import logging
from logging import Logger
from logging.handlers import RotatingFileHandler
import os

"""
Logging setup for the application.

- Creates a `logs/` directory if it doesn't exist.
- Sets up both console and file logging with rotation.
- File logs are stored in 'logs/app.log' and rotate at 10MB with 5 backups.
"""

def setup_logging() -> Logger:
    """
    Configures and returns the application's root logger.

    Returns:
        Logger: The configured logger instance.
    """
    log_dir = 'logs'
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, 'app.log')

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    if not logger.handlers:
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=10 * 1024 * 1024,  # 10 MB
            backupCount=5
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger
