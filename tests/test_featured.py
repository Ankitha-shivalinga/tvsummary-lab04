from tvsummary.featured import pick_featured_shows
from tvsummary.models import ShowRecord


def test_the_same_seed_gives_the_same_list(records):
    first = pick_featured_shows(records, 3, seed=42)
    second = pick_featured_shows(records, 3, seed=42)

    assert first == second


def test_a_known_seed_gives_a_known_list(records):
    assert pick_featured_shows(records, 2, seed=42) == ["Alpha", "Delta"]


def test_the_list_never_has_more_names_than_there_are_shows(records):
    assert len(pick_featured_shows(records, 10, seed=1)) == len(records)


def test_shows_without_a_name_are_never_featured():
    records = [ShowRecord({"name": ""}), ShowRecord({"name": "Alpha"})]
    assert pick_featured_shows(records, 2, seed=3) == ["Alpha"]


def test_the_records_are_not_changed(records):
    before = [record.name for record in records]
    pick_featured_shows(records, 3, seed=5)
    assert [record.name for record in records] == before
