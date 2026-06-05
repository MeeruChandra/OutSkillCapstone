import logging
import sys
from pathlib import Path
from logging.handlers import RotatingFileHandler
from datetime import datetime


class LoggerSetup:
    """
    Centralized logging configuration for the e-commerce API.
    Provides structured logging with file rotation and console output.
    """

    @staticmethod
    def setup_logger(
        name: str = "ecommerce_api",
        log_level: str = "INFO",
        log_dir: str = "logs",
        max_bytes: int = 10485760,
        backup_count: int = 5
    ) -> logging.Logger:
        """
        Set up logger with file and console handlers.

        Args:
            name: Logger name
            log_level: Logging level (DEBUG, INFO, WARNING, ERROR)
            log_dir: Directory for log files
            max_bytes: Maximum size of log file before rotation (default 10MB)
            backup_count: Number of backup files to keep

        Returns:
            Configured logger instance
        """
        logger = logging.getLogger(name)

        if logger.handlers:
            return logger

        logger.setLevel(getattr(logging, log_level.upper()))

        log_path = Path(log_dir)
        log_path.mkdir(exist_ok=True)

        formatter = logging.Formatter(
            fmt='%(asctime)s - %(name)s - %(levelname)s - %(module)s:%(funcName)s:%(lineno)d - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

        file_handler = RotatingFileHandler(
            filename=log_path / f"ecommerce_api_{datetime.now().strftime('%Y%m%d')}.log",
            maxBytes=max_bytes,
            backupCount=backup_count,
            encoding='utf-8'
        )
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)

        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)

        error_file_handler = RotatingFileHandler(
            filename=log_path / f"ecommerce_api_errors_{datetime.now().strftime('%Y%m%d')}.log",
            maxBytes=max_bytes,
            backupCount=backup_count,
            encoding='utf-8'
        )
        error_file_handler.setLevel(logging.ERROR)
        error_file_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        logger.addHandler(error_file_handler)

        return logger


def get_logger(name: str = "ecommerce_api") -> logging.Logger:
    """
    Get or create a logger instance.

    Args:
        name: Logger name (default: ecommerce_api)

    Returns:
        Logger instance
    """
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger = LoggerSetup.setup_logger(name)
    return logger
