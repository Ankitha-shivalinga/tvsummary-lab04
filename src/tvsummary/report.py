"""Build the TV show summary and write it, with a record of the run."""

import json
import logging
import platform
from collections.abc import Sequence
from dataclasses import asdict
from importlib import metadata
from pathlib import Path

from tvsummary.aggregations import Aggregation, DecadeAggregation, GenreAggregation
from tvsummary.config import Settings
from tvsummary.errors import ReportError
from tvsummary.models import ShowRecord

logger = logging.getLogger(__name__)

RECORDED_PACKAGES = ("requests", "pytest", "mypy", "ruff")


def build_summary(
    source_url: str, records: Sequence[ShowRecord], featured_shows: list[str]
) -> dict[str, object]:
    """Return the summary: the Lab 03 keys, then the featured shows."""
    summary: dict[str, object] = {
        "source_url": source_url,
        "total_records": len(records),
    }

    aggregations: list[Aggregation] = [
        GenreAggregation(records),
        DecadeAggregation(records),
    ]

    for aggregation in aggregations:
        summary[aggregation.summary_key] = aggregation.aggregate()

    summary["featured_shows"] = featured_shows
    return summary


def build_run_info(settings: Settings) -> dict[str, object]:
    """Return the settings, Python version and package versions of this run."""
    settings_used = asdict(settings)
    settings_used["output_dir"] = settings.output_dir.as_posix()

    return {
        "settings": settings_used,
        "python": platform.python_version(),
        "packages": {name: _package_version(name) for name in RECORDED_PACKAGES},
    }


def _package_version(name: str) -> str:
    """Return the installed version of a package, or say it is missing."""
    try:
        return metadata.version(name)
    except metadata.PackageNotFoundError:
        return "not installed"


class ReportWriter:
    """Write summary data to JSON files in one folder."""

    def __init__(self, output_dir: Path) -> None:
        """Initialize the report writer."""
        self.output_dir = output_dir

    def write(self, file_name: str, data: dict[str, object]) -> Path:
        """Save the data as formatted JSON and return the file's path."""
        path = self.output_dir / file_name

        try:
            self.output_dir.mkdir(parents=True, exist_ok=True)
            path.write_text(json.dumps(data, indent=2), encoding="utf-8")
        except OSError as error:
            raise ReportError(f"Cannot write {path}: {error.strerror}") from error

        logger.info("Wrote %s", path)
        return path
