
"""Aggregate TV show records into summary counts."""


class Aggregation:
    """Base class for show aggregations."""

    def __init__(self, records):
        """Initialize the aggregation with show records."""
        self.records = records

    def aggregate(self):
        """Return the aggregation result."""
        raise NotImplementedError("Subclasses must implement aggregate().")

    @property
    def summary_key(self):
        """Return the key used for this aggregation."""
        raise NotImplementedError("Subclasses must implement summary_key.")


class GenreAggregation(Aggregation):
    """Count shows in each genre."""

    def aggregate(self):
        """Return counts grouped by genre."""
        counts = {}

        for record in self.records:
            for genre in record.genres:
                counts[genre] = counts.get(genre, 0) + 1

        return counts
    
    @property
    def summary_key(self):
        """Return the genre summary key."""
        return "shows_per_genre"
    

class DecadeAggregation(Aggregation):
    """Count shows by premiere decade."""

    def aggregate(self):
        """Return counts grouped by decade."""
        counts = {}

        for record in self.records:
            premiered = record.premiered

            if len(premiered) < 4:
                continue

            try:
                year = int(premiered[:4])
            except ValueError:
                continue

            decade = (year // 10) * 10
            label = f"{decade}s"
            counts[label] = counts.get(label, 0) + 1

        return counts

    @property
    def summary_key(self):
        """Return the decade summary key."""
        return "shows_per_decade"


    
