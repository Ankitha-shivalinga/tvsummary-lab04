"""Run the TV show summary program: python -m tvsummary.main"""

import argparse
import logging
import sys
from pathlib import Path

from tvsummary.config import DEFAULT_CONFIG_PATH, load_settings
from tvsummary.errors import TVSummaryError
from tvsummary.featured import pick_featured_shows
from tvsummary.logging_setup import configure_logging, set_log_level
from tvsummary.report import ReportWriter, build_run_info, build_summary
from tvsummary.sources import TVMazeSource

logger = logging.getLogger(__name__)


def parse_args(argv: list[str] | None) -> argparse.Namespace:
    """Read the command line options."""
    parser = argparse.ArgumentParser(
        description="Summarize TV show records from the TVMaze API."
    )
    parser.add_argument(
        "--config",
        type=Path,
        default=DEFAULT_CONFIG_PATH,
        help=f"path to the settings file (default: {DEFAULT_CONFIG_PATH})",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    """Run the program and return its exit code (0 means success)."""
    args = parse_args(argv)
    configure_logging("INFO")

    try:
        settings = load_settings(args.config)
        set_log_level(settings.log_level)
        logger.info("Read settings from %s", args.config)

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
        return 1

    print(f"Summary saved to {summary_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
