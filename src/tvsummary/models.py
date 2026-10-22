"""The record class for one TV show."""


class ShowRecord:
    """Represent one TV show record and clean its data."""

    def __init__(self, record: object) -> None:
        """Initialize a show record with safe default values."""
        data = record if isinstance(record, dict) else {}

        self.name = self._clean_text(data.get("name"))
        self.genres = self._clean_genres(data.get("genres"))
        self.premiered = self._clean_text(data.get("premiered"))
        self.rating = self._clean_rating(data.get("rating"))

    def _clean_text(self, value: object) -> str:
        """Return cleaned text or an empty string."""
        if not isinstance(value, str):
            return ""

        return value.strip()

    def _clean_genres(self, value: object) -> list[str]:
        """Return a list of valid genre names."""
        if not isinstance(value, list):
            return []

        genres = []

        for genre in value:
            if isinstance(genre, str) and genre.strip():
                genres.append(genre.strip())

        return sorted(set(genres))

    def _clean_rating(self, value: object) -> float | None:
        """Return the average rating as a float, or None when there is none."""
        if not isinstance(value, dict):
            return None

        average = value.get("average")

        if isinstance(average, bool) or not isinstance(average, int | float):
            return None

        return float(average)

    def __str__(self) -> str:
        """Return a readable description of the show."""
        return self.name or "Unknown show"
