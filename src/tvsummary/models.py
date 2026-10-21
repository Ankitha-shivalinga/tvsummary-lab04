
class ShowRecord:
    """Represent one TV show record and clean its data."""

    def __init__(self, record):
        """Initialize a show record with safe default values."""
        if not isinstance(record, dict):
            record = {}

        self.name = self._clean_text(record.get("name"))
        self.genres = self._clean_genres(record.get("genres"))
        self.premiered = self._clean_text(record.get("premiered"))

    def _clean_text(self, value):
        """Return cleaned text or an empty string."""
        if not isinstance(value, str):
            return ""

        return value.strip()

    def _clean_genres(self, value):
        """Return a list of valid genre names."""
        if not isinstance(value, list):
            return []

        genres = []

        for genre in value:
            if isinstance(genre, str) and genre.strip():
                genres.append(genre.strip())

        return sorted(set(genres))

    def __str__(self):
        """Return a readable description of the show."""
        return self.name or "Unknown show"
