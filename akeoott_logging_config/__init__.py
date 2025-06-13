__version__ = "1.2.1"
__author__ = "Akeoott/Akeoottt"
__description__ = "A simple yet robust logging configuration library for Python applications."

from .logging_config import LogConfig

__all__ = [
    "LogConfig", # Expose the LogConfig class
]