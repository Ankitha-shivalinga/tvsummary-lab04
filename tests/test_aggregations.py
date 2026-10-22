import pytest

from tvsummary.aggregations import Aggregation, DecadeAggregation, GenreAggregation
from tvsummary.models import ShowRecord


def test_genres_are_counted(records):
    assert GenreAggregation(records).aggregate() == {"Drama": 2, "Comedy": 2}


def test_decades_are_counted(records):
    assert DecadeAggregation(records).aggregate() == {
        "2010s": 2,
        "2000s": 1,
        "1990s": 1,
    }


def test_a_show_without_a_usable_premiere_is_left_out():
    records = [
        ShowRecord({"name": "No date", "premiered": None}),
        ShowRecord({"name": "Bad date", "premiered": "soon"}),
        ShowRecord({"name": "Good", "premiered": "2001-02-03"}),
    ]
    assert DecadeAggregation(records).aggregate() == {"2000s": 1}


def test_no_records_give_empty_counts():
    assert GenreAggregation([]).aggregate() == {}
    assert DecadeAggregation([]).aggregate() == {}


@pytest.mark.parametrize(
    ("aggregation_class", "key"),
    [(GenreAggregation, "shows_per_genre"), (DecadeAggregation, "shows_per_decade")],
)
def test_each_aggregation_has_its_summary_key(aggregation_class, key):
    assert aggregation_class([]).summary_key == key


def test_the_base_class_must_be_subclassed():
    with pytest.raises(NotImplementedError, match="Subclasses"):
        Aggregation([]).aggregate()
