import json

import requests

from tvsummary import sources
from tvsummary.main import main


class FakeResponse:
    """A successful response holding two shows."""

    status_code = 200

    def raise_for_status(self):
        pass

    def json(self):
        return [
            {"name": "Alpha", "genres": ["Drama"], "premiered": "2014-06-24"},
            {"name": "Bravo", "genres": ["Comedy"], "premiered": "2009-01-05"},
        ]


def test_a_missing_settings_file_exits_with_one(tmp_path, capsys):
    exit_code = main(["--config", str(tmp_path / "none.toml")])

    error_output = capsys.readouterr().err
    assert exit_code == 1
    assert error_output.startswith("Error: Cannot read the settings file")
    assert "Traceback" not in error_output


def test_a_failed_download_exits_with_one(settings_file, monkeypatch, capsys):
    def fake_get(*args, **kwargs):
        raise requests.ConnectionError("no network")

    monkeypatch.setattr(sources.requests, "get", fake_get)

    exit_code = main(["--config", str(settings_file)])

    assert exit_code == 1
    assert capsys.readouterr().err.startswith("Error: Could not reach")


def test_a_successful_run_writes_both_files(settings_file, monkeypatch, capsys):
    monkeypatch.setattr(sources.requests, "get", lambda *a, **k: FakeResponse())

    exit_code = main(["--config", str(settings_file)])

    output_dir = settings_file.parent / "processed"
    summary = json.loads((output_dir / "summary.json").read_text(encoding="utf-8"))
    assert exit_code == 0
    assert summary["total_records"] == 2
    assert len(summary["featured_shows"]) == 2
    assert (output_dir / "run_info.json").exists()
    assert "Summary saved to" in capsys.readouterr().out
