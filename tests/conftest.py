"""Shared fixtures for the tvsummary tests."""

import pytest

from tvsummary.models import ShowRecord


@pytest.fixture
def records():
    return [
        ShowRecord({"name": "Alpha", "genres": ["Drama"], "premiered": "2014-06-24"}),
        ShowRecord(
            {"name": "Bravo", "genres": ["Drama", "Comedy"], "premiered": "2009-01-05"}
        ),
        ShowRecord({"name": "Charlie", "genres": [], "premiered": "1999-09-01"}),
        ShowRecord({"name": "Delta", "genres": ["Comedy"], "premiered": "2011-03-10"}),
    ]
