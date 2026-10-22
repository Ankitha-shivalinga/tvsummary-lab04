"""Download TV show records from the TVMaze API."""

import logging

import requests

from tvsummary.errors import ResponseFormatError, SourceError
from tvsummary.models import ShowRecord

logger = logging.getLogger(__name__)


def parse_records(data: object) -> list[ShowRecord]:
    """Turn the decoded API response into ShowRecord objects."""
    if not isinstance(data, list):
        raise ResponseFormatError(
            f"Expected a list of shows, but the response was a {type(data).__name__}."
        )

    logger.debug("Received %d show records", len(data))
    return [ShowRecord(record) for record in data]


class TVMazeSource:
    """Fetch TV show records from TVMaze."""

    def __init__(self, url: str, timeout: float) -> None:
        """Initialize the data source."""
        self.url = url
        self.timeout = timeout

    def download(self) -> object:
        """Download the shows and return the decoded JSON."""
        logger.info("Downloading shows from %s", self.url)

        try:
            response = requests.get(self.url, timeout=self.timeout)
        except requests.RequestException as error:
            raise SourceError(f"Could not reach {self.url}: {error}") from error

        try:
            response.raise_for_status()
        except requests.HTTPError as error:
            raise SourceError(
                f"{self.url} answered with HTTP {response.status_code}."
            ) from error

        try:
            return response.json()
        except ValueError as error:
            raise ResponseFormatError(
                f"The response from {self.url} is not valid JSON."
            ) from error

    def fetch_records(self) -> list[ShowRecord]:
        """Download records and return ShowRecord objects."""
        return parse_records(self.download())
