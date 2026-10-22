"""Shared fixtures for the tvsummary tests."""

from pathlib import Path

import pytest

from tvsummary.models import ShowRecord

SETTINGS_TEXT = """
source_url = "https://example.invalid/shows"
timeout = 5
output_dir = "{output_dir}"
seed = 7
sample_size = 2
log_level = "DEBUG"
"""


@pytest.fixture
def records() -> list[ShowRecord]:
    return [
        ShowRecord({"name": "Alpha", "genres": ["Drama"], "premiered": "2014-06-24"}),
        ShowRecord(
            {"name": "Bravo", "genres": ["Drama", "Comedy"], "premiered": "2009-01-05"}
        ),
        ShowRecord({"name": "Charlie", "genres": [], "premiered": "1999-09-01"}),
        ShowRecord({"name": "Delta", "genres": ["Comedy"], "premiered": "2011-03-10"}),
    ]


@pytest.fixture
def settings_file(tmp_path: Path) -> Path:
    path = tmp_path / "tvsummary.toml"
    output_dir = (tmp_path / "processed").as_posix()
    path.write_text(SETTINGS_TEXT.format(output_dir=output_dir), encoding="utf-8")
    return path
