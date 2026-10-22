import json
import platform

import pytest

from tvsummary.config import load_settings
from tvsummary.errors import ReportError
from tvsummary.report import ReportWriter, build_run_info, build_summary


def test_the_summary_keeps_the_lab_03_keys_and_adds_featured_shows(records):
    summary = build_summary("https://example.invalid", records, ["Alpha"])

    assert list(summary) == [
        "source_url",
        "total_records",
        "shows_per_genre",
        "shows_per_decade",
        "featured_shows",
    ]
    assert summary["total_records"] == 4
    assert summary["featured_shows"] == ["Alpha"]


def test_run_info_records_settings_and_versions(settings_file):
    settings = load_settings(settings_file)

    run_info = build_run_info(settings)

    assert run_info["settings"]["seed"] == 7
    assert run_info["python"] == platform.python_version()
    assert set(run_info["packages"]) == {"requests", "pytest", "mypy", "ruff"}
    assert json.loads(json.dumps(run_info)) == run_info


def test_a_file_is_written_as_json(tmp_path):
    path = ReportWriter(tmp_path / "processed").write("summary.json", {"total": 2})

    assert path == tmp_path / "processed" / "summary.json"
    assert json.loads(path.read_text(encoding="utf-8")) == {"total": 2}


def test_an_unwritable_folder_raises_a_report_error(tmp_path):
    blocker = tmp_path / "processed"
    blocker.write_text("a file, not a folder", encoding="utf-8")

    with pytest.raises(ReportError, match="Cannot write"):
        ReportWriter(blocker).write("summary.json", {})
