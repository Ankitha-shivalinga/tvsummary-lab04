
"""Download TV show records from the TVMaze API."""

import requests

from tvsummary.config import SOURCE_URL, TIMEOUT
from tvsummary.models import ShowRecord


class TVMazeSource:
    """Fetch TV show records from TVMaze."""

    def __init__(self, url=SOURCE_URL, timeout=TIMEOUT):
        """Initialize the data source."""
        self.url = url
        self.timeout = timeout

    def fetch_records(self):
        """Download records and return ShowRecord objects."""
        try:
            response = requests.get(self.url, timeout=self.timeout)
            response.raise_for_status()
            records = response.json()
        except requests.RequestException as error:
            raise RuntimeError(f"Error downloading data: {error}") from None
        except ValueError as error:
            raise RuntimeError(f"Error reading API response: {error}") from None

        if not isinstance(records, list):
            raise RuntimeError("Error reading API response: expected a list of records.")

        return [ShowRecord(record) for record in records]
