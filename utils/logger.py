import logging
import sys
from pythonjsonlogger import jsonlogger
from pathlib import Path
from datetime import datetime

def setup_logger(name: str, log_file: str = None):
    """
    Setup structured JSON logger for production
    
    Usage:
        logger = setup_logger(__name__)
        logger.info("User signed up", extra={"email": "user@example.com"})
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    # Remove any existing handlers to avoid duplicates
    logger.handlers.clear()
    
    # Console handler (human-readable)
    console_handler = logging.StreamHandler(sys.stdout)
    console_format = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    console_handler.setFormatter(console_format)
    logger.addHandler(console_handler)
    
    # File handler (JSON format)
    if log_file:
        Path("logs").mkdir(exist_ok=True)
        file_handler = logging.FileHandler(f"logs/{log_file}")
        
        # FIX: Use correct field names for JSON formatter
        json_format = jsonlogger.JsonFormatter(
            '%(asctime)s %(levelname)s %(name)s %(message)s',
            rename_fields={
                'asctime': 'timestamp',
                'levelname': 'level'
            },
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(json_format)
        logger.addHandler(file_handler)
    
    # Prevent propagation to root logger
    logger.propagate = False
    
    return logger

# Usage in your code
if __name__ == "__main__":
    logger = setup_logger("test", "test.log")
    logger.info("Test message", extra={"user_id": 123, "action": "test"})
    print("Check logs/test.log for JSON output")