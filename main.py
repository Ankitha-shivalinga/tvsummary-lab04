"""Run the TV show summary program."""

import logging
import sys

from tvsummary.aggregations import (
    DecadeAggregation,
    GenreAggregation,
)
from tvsummary.config import OUTPUT_PATH, SOURCE_URL, TIMEOUT
from tvsummary.errors import TVSummaryError
from tvsummary.logging_setup import configure_logging
from tvsummary.report import ReportWriter
from tvsummary.sources import TVMazeSource

logger = logging.getLogger(__name__)


def main():
    """Download show records and write their summary."""
    configure_logging("INFO")
    source = TVMazeSource(SOURCE_URL, TIMEOUT)

    try:
        records = source.fetch_records()

        aggregations = [
            GenreAggregation(records),
            DecadeAggregation(records),
        ]

        summary = {
            "source_url": SOURCE_URL,
            "total_records": len(records),
        }

        for aggregation in aggregations:
            summary[aggregation.summary_key] = aggregation.aggregate()

        writer = ReportWriter(OUTPUT_PATH)
        writer.write(summary)
    except TVSummaryError as error:
        logger.error("Stopped: %s", error)
        print(f"Error: {error}", file=sys.stderr)
        return

    print(f"Summary saved to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
