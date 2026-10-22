"""Choose a few featured shows with a seeded random generator."""

import logging
import random
from collections.abc import Sequence

from tvsummary.models import ShowRecord

logger = logging.getLogger(__name__)


def pick_featured_shows(
    records: Sequence[ShowRecord], count: int, seed: int
) -> list[str]:
    """Return up to count show names, chosen the same way for the same seed."""
    names = [record.name for record in records if record.name]
    generator = random.Random(seed)
    featured = generator.sample(names, k=min(count, len(names)))

    logger.info("Chose %d featured shows with seed %d", len(featured), seed)
    return featured
