import time
import logging
from functools import wraps

logger = logging.getLogger(__name__)

def retry_on_failure(max_retries=3, delay=2, backoff=2):
    """Retry decorator with exponential backoff"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            retries = 0
            current_delay = delay
            
            while retries < max_retries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    retries += 1
                    if retries >= max_retries:
                        logger.error(f"Failed after {max_retries} retries: {str(e)}")
                        raise
                    
                    logger.warning(f"Attempt {retries} failed: {str(e)}. Retrying in {current_delay}s...")
                    time.sleep(current_delay)
                    current_delay *= backoff
            
        return wrapper
    return decorator