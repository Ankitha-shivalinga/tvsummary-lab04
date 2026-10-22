"""Public classes and functions for the TV summary package."""

from tvsummary.aggregations import (
    Aggregation,
    DecadeAggregation,
    GenreAggregation,
)
from tvsummary.config import Settings, load_settings
from tvsummary.errors import (
    ReportError,
    ResponseFormatError,
    SettingsError,
    SourceError,
    TVSummaryError,
)
from tvsummary.featured import pick_featured_shows
from tvsummary.models import ShowRecord
from tvsummary.report import ReportWriter, build_run_info, build_summary
from tvsummary.sources import TVMazeSource, parse_records

__all__ = [
    "Aggregation",
    "DecadeAggregation",
    "GenreAggregation",
    "ReportError",
    "ReportWriter",
    "ResponseFormatError",
    "Settings",
    "SettingsError",
    "ShowRecord",
    "SourceError",
    "TVMazeSource",
    "TVSummaryError",
    "build_run_info",
    "build_summary",
    "load_settings",
    "parse_records",
    "pick_featured_shows",
]
