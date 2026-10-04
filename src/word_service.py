"""Word service for loading and selecting target words."""

import json
import random
from pathlib import Path


def load_words(filepath: str | Path | None = None) -> list[str]:
    """Load 5-letter words from JSON file."""
    if filepath is None:
        base_dir = Path(__file__).resolve().parent.parent
        filepath = base_dir / "data" / "words.json"

    filepath = Path(filepath)
    if not filepath.exists():
        return []

    with filepath.open("r", encoding="utf-8-sig") as f:
        words = json.load(f)

    normalized = [str(w).upper().strip() for w in words]
    valid_words = [w for w in normalized if len(w) == 5 and w.isalpha()]
    return valid_words


def get_random_word(words: list[str]) -> str:
    """Select a random word from word list."""
    if not words:
        raise ValueError("Word list is empty")
    return random.choice(words)
