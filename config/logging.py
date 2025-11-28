import logging
from pathlib import Path
from .app import settings

LOG_DIR = Path("storage/logs")
LOG_DIR.mkdir(exist_ok=True)

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "file": {
            "level": "DEBUG" if settings.debug else "INFO",
            "class": "logging.FileHandler",
            "filename": LOG_DIR / "app.log",
            "formatter": "verbose",
        },
    },
    "root": {
        "handlers": ["file"],
        "level": "DEBUG",
    },
}