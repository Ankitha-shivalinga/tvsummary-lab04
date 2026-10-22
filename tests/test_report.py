import json

import pytest

from tvsummary.errors import ReportError
from tvsummary.report import ReportWriter


def test_the_summary_is_written_as_json(tmp_path):
    path = tmp_path / "processed" / "summary.json"

    ReportWriter(path).write({"total_records": 2})

    assert json.loads(path.read_text(encoding="utf-8")) == {"total_records": 2}


def test_an_unwritable_folder_raises_a_report_error(tmp_path):
    blocker = tmp_path / "processed"
    blocker.write_text("a file, not a folder", encoding="utf-8")

    with pytest.raises(ReportError, match="Cannot write"):
        ReportWriter(blocker / "summary.json").write({})
