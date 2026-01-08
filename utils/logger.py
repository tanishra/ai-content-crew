import logging
from pythonjsonlogger import jsonlogger

def setup_logger(name):
    logger = logging.getLogger(name)
    handler = logging.FileHandler('logs/app.json')
    
    formatter = jsonlogger.JsonFormatter(
        '%(timestamp)s %(level)s %(name)s %(message)s'
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    
    return logger