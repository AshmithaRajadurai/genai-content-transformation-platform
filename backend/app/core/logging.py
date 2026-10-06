import logging
import sys


def setup_logging(level: int = logging.INFO) -> None:
    """Configure centralized structured logging format."""
    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] [%(name)s]: %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout),
        ],
    )


def get_logger(name: str) -> logging.Logger:
    """Return a logger configured with the given name."""
    return logging.getLogger(name)
