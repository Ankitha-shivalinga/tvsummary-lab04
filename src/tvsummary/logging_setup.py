"""Configure logging for the tvsummary program."""

import logging

LOG_FORMAT = "%(asctime)s %(levelname)-8s %(name)s: %(message)s"


def configure_logging(level: str) -> None:
    """Send log messages at the given level and above to standard error."""
    logging.basicConfig(level=level, format=LOG_FORMAT)


def set_log_level(level: str) -> None:
    """Change the level once the settings file has been read."""
    logging.getLogger().setLevel(level)
