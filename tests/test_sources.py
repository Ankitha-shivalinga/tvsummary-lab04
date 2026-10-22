import pytest
import requests

from tvsummary import sources
from tvsummary.errors import ResponseFormatError, SourceError
from tvsummary.sources import TVMazeSource, parse_records


class FakeResponse:
    """Stand in for requests.Response with a fixed status and body."""

    def __init__(self, status_code=200, body=None, valid_json=True):
        self.status_code = status_code
        self.body = body
        self.valid_json = valid_json

    def raise_for_status(self):
        if self.status_code >= 400:
            raise requests.HTTPError(f"{self.status_code} error")

    def json(self):
        if not self.valid_json:
            raise ValueError("Expecting value")
        return self.body


def use_fake_get(monkeypatch, response):
    def fake_get(*args, **kwargs):
        return response

    monkeypatch.setattr(sources.requests, "get", fake_get)


def test_a_failed_download_raises_a_source_error(monkeypatch):
    def fake_get(*args, **kwargs):
        raise requests.ConnectionError("no network")

    monkeypatch.setattr(sources.requests, "get", fake_get)

    with pytest.raises(SourceError, match="reach"):
        TVMazeSource("https://example.invalid", timeout=1).fetch_records()


def test_an_http_error_raises_a_source_error(monkeypatch):
    use_fake_get(monkeypatch, FakeResponse(status_code=503))

    with pytest.raises(SourceError, match="HTTP 503"):
        TVMazeSource("https://example.invalid", timeout=1).fetch_records()


def test_a_response_that_is_not_json_raises_a_format_error(monkeypatch):
    use_fake_get(monkeypatch, FakeResponse(valid_json=False))

    with pytest.raises(ResponseFormatError, match="not valid JSON"):
        TVMazeSource("https://example.invalid", timeout=1).fetch_records()


def test_a_good_response_becomes_records(monkeypatch):
    use_fake_get(monkeypatch, FakeResponse(body=[{"name": "Alpha"}, {"name": "Bravo"}]))

    records = TVMazeSource("https://example.invalid", timeout=1).fetch_records()

    assert [record.name for record in records] == ["Alpha", "Bravo"]


@pytest.mark.parametrize("data", [{"name": "Alpha"}, "text", None])
def test_data_that_is_not_a_list_raises_a_format_error(data):
    with pytest.raises(ResponseFormatError, match="Expected a list"):
        parse_records(data)
