"""Aggregate TV show records into summary counts."""

import logging
from collections.abc import Sequence

from tvsummary.models import ShowRecord

logger = logging.getLogger(__name__)


class Aggregation:
    """Base class for show aggregations."""

    def __init__(self, records: Sequence[ShowRecord]) -> None:
        """Initialize the aggregation with show records."""
        self.records = records

    def aggregate(self) -> dict[str, int]:
        """Return the aggregation result."""
        raise NotImplementedError("Subclasses must implement aggregate().")

    @property
    def summary_key(self) -> str:
        """Return the key used for this aggregation."""
        raise NotImplementedError("Subclasses must implement summary_key.")


class GenreAggregation(Aggregation):
    """Count shows in each genre."""

    def aggregate(self) -> dict[str, int]:
        """Return counts grouped by genre."""
        counts: dict[str, int] = {}

        for record in self.records:
            for genre in record.genres:
                counts[genre] = counts.get(genre, 0) + 1

        return counts

    @property
    def summary_key(self) -> str:
        """Return the genre summary key."""
        return "shows_per_genre"


class DecadeAggregation(Aggregation):
    """Count shows by premiere decade."""

    def aggregate(self) -> dict[str, int]:
        """Return counts grouped by decade."""
        counts: dict[str, int] = {}

        for record in self.records:
            year = self._premiere_year(record)

            if year is None:
                logger.warning(
                    "Skipping %s: premiere date %r is not usable",
                    record,
                    record.premiered,
                )
                continue

            decade = (year // 10) * 10
            label = f"{decade}s"
            counts[label] = counts.get(label, 0) + 1

        return counts

    def _premiere_year(self, record: ShowRecord) -> int | None:
        """Return the premiere year, or None when the date cannot be read."""
        if len(record.premiered) < 4:
            return None

        try:
            return int(record.premiered[:4])
        except ValueError:
            return None

    @property
    def summary_key(self) -> str:
        """Return the decade summary key."""
        return "shows_per_decade"
