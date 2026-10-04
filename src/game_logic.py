"""Game logic for Wordle evaluation."""

from src.constants import (
    STATUS_ABSENT,
    STATUS_CORRECT,
    STATUS_PRESENT,
    WORD_LENGTH,
)


def evaluate_guess(target: str, guess: str) -> list[dict[str, str]]:
    """Evaluate a guess against target word.

    Uses standard Wordle algorithm:
    1. First pass: mark correct positions (green).
    2. Second pass: mark present letters (yellow) using remaining counts.

    Args:
        target: The target word (uppercase, 5 letters).
        guess: The guessed word (uppercase, 5 letters).

    Returns:
        List of dicts with keys: "index", "letter", "status".
        Status values: "correct", "present", "absent".
    """
    if len(target) != WORD_LENGTH:
        target = target[:WORD_LENGTH].upper()
    if len(guess) != WORD_LENGTH:
        guess = guess[:WORD_LENGTH].upper()

    target_upper = target.upper()
    guess_upper = guess.upper()

    result: list[dict[str, str]] = [
        {"index": i, "letter": guess_upper[i], "status": STATUS_ABSENT}
        for i in range(WORD_LENGTH)
    ]

    # Count remaining letters in target (for present/yellow)
    remaining_counts: dict[str, int] = {}
    for c in target_upper:
        remaining_counts[c] = remaining_counts.get(c, 0) + 1

    # First pass: mark correct (green)
    for i in range(WORD_LENGTH):
        if guess_upper[i] == target_upper[i]:
            result[i]["status"] = STATUS_CORRECT
            remaining_counts[guess_upper[i]] = (
                remaining_counts.get(guess_upper[i], 0) - 1
            )
            remaining_counts[guess_upper[i]] = max(remaining_counts[guess_upper[i]], 0)

    # Second pass: mark present (yellow)
    for i in range(WORD_LENGTH):
        if result[i]["status"] == STATUS_CORRECT:
            continue
        letter = guess_upper[i]
        if remaining_counts.get(letter, 0) > 0:
            result[i]["status"] = STATUS_PRESENT
            remaining_counts[letter] = remaining_counts.get(letter, 0) - 1

    return result


def is_correct_guess(evaluation: list[dict[str, str]]) -> bool:
    """Check if evaluation represents a correct guess.

    Args:
        evaluation: Result from evaluate_guess.

    Returns:
        True if all letters are correct.
    """
    if not evaluation:
        return False
    return all(item["status"] == STATUS_CORRECT for item in evaluation)
