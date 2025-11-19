import logging

from typing import Optional

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
def get_logger(name: Optional[str]) -> logging.Logger:
    """Get a logger instance by name"""
    if  name is None:
        name = "cbon"
    return logging.getLogger(name)