
"""Public classes for the TV summary package."""

from tvsummary.aggregations import (
    Aggregation,
    DecadeAggregation,
    GenreAggregation,
)
from tvsummary.models import ShowRecord
from tvsummary.report import ReportWriter
from tvsummary.sources import TVMazeSource

__all__ = [
    "Aggregation",
    "DecadeAggregation",
    "GenreAggregation",
    "ReportWriter",
    "ShowRecord",
    "TVMazeSource",
]
