__version__ = "1.0.0"
__author__ = "Akeoott/Akeoottt"
__description__ = "A simple yet robust logging configuration library for Python applications."

from .logging_config import setup_library_logging, get_library_logger

__all__ = [
    "setup_library_logging",
    "get_library_logger",
]