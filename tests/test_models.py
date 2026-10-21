import unittest
from tvsummary.models import ShowRecord


class TestShowRecord(unittest.TestCase):
    def test_missing_genres(self):
        record = ShowRecord({
            "name": "Test Show",
            "genres": None
        })

        self.assertEqual(record.genres, [])

    def test_show_name(self):
        record = ShowRecord({
            "name": "Test Show",
            "genres": []
        })

        self.assertEqual(str(record), "Test Show")
        
if __name__ == "__main__":
    unittest.main()