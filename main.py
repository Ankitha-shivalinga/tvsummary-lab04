
"""Run the TV show summary program."""


from tvsummary.aggregations import (
    DecadeAggregation,
    GenreAggregation,
)
from tvsummary.config import OUTPUT_PATH, SOURCE_URL, TIMEOUT
from tvsummary.report import ReportWriter
from tvsummary.sources import TVMazeSource


def main():
    """Download show records and write their summary."""
    source = TVMazeSource(SOURCE_URL, TIMEOUT)

    try:
        records = source.fetch_records()
    except RuntimeError as error:
        print(error)
        return
    
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
    print(f"Summary saved to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
