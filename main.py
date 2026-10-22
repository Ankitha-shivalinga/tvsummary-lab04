"""Run the TV show summary program."""

import logging
import sys

from tvsummary.config import DEFAULT_CONFIG_PATH, load_settings
from tvsummary.errors import TVSummaryError
from tvsummary.featured import pick_featured_shows
from tvsummary.logging_setup import configure_logging, set_log_level
from tvsummary.report import ReportWriter, build_run_info, build_summary
from tvsummary.sources import TVMazeSource

logger = logging.getLogger(__name__)


def main():
    """Download show records and write their summary."""
    configure_logging("INFO")

    try:
        settings = load_settings(DEFAULT_CONFIG_PATH)
        set_log_level(settings.log_level)

        source = TVMazeSource(settings.source_url, settings.timeout)
        records = source.fetch_records()

        featured = pick_featured_shows(records, settings.sample_size, settings.seed)
        summary = build_summary(settings.source_url, records, featured)

        writer = ReportWriter(settings.output_dir)
        summary_path = writer.write("summary.json", summary)
        writer.write("run_info.json", build_run_info(settings))
    except TVSummaryError as error:
        logger.error("Stopped: %s", error)
        print(f"Error: {error}", file=sys.stderr)
        return

    print(f"Summary saved to {summary_path}")


if __name__ == "__main__":
    main()
