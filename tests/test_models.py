import pytest

from tvsummary.models import ShowRecord


def test_a_missing_genre_list_becomes_empty():
    record = ShowRecord({"name": "Test Show", "genres": None})
    assert record.genres == []


def test_genres_are_stripped_sorted_and_unique():
    record = ShowRecord({"name": "Test Show", "genres": [" Drama", "Comedy", "Drama"]})
    assert record.genres == ["Comedy", "Drama"]


def test_the_show_name_is_its_text():
    record = ShowRecord({"name": "  Test Show  ", "genres": []})
    assert str(record) == "Test Show"


@pytest.mark.parametrize("bad_record", [None, "a string", 42, []])
def test_a_record_that_is_not_a_dict_gets_safe_defaults(bad_record):
    record = ShowRecord(bad_record)
    assert record.name == ""
    assert record.genres == []
    assert str(record) == "Unknown show"


def test_a_rating_is_read_from_the_average():
    record = ShowRecord({"name": "Test Show", "rating": {"average": 8.5}})
    assert record.rating == 8.5


@pytest.mark.parametrize(
    "rating", [None, {}, {"average": None}, {"average": "high"}, 7.0]
)
def test_a_missing_rating_becomes_none(rating):
    record = ShowRecord({"name": "Test Show", "rating": rating})
    assert record.rating is None
