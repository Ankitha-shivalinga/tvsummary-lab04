"""Write the TV show summary to a JSON file."""

import json
from pathlib import Path

from tvsummary.errors import ReportError


class ReportWriter:
    """Write summary data to a JSON file."""

    def __init__(self, output_path):
        """Initialize the report writer."""
        self.output_path = Path(output_path)

    def write(self, summary):
        """Save the summary as formatted JSON."""
        try:
            self.output_path.parent.mkdir(parents=True, exist_ok=True)
            self.output_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
        except OSError as error:
            raise ReportError(
                f"Cannot write {self.output_path}: {error.strerror}"
            ) from error
