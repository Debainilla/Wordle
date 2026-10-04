"""Tests for game logic."""

from src.constants import STATUS_ABSENT, STATUS_CORRECT, STATUS_PRESENT
from src.game_logic import evaluate_guess, is_correct_guess


def test_all_green():
    target = "APPLE"
    guess = "APPLE"
    result = evaluate_guess(target, guess)
    assert all(item["status"] == STATUS_CORRECT for item in result)
    assert is_correct_guess(result) is True


def test_all_gray():
    target = "APPLE"
    guess = "STORM"
    result = evaluate_guess(target, guess)
    assert all(item["status"] == STATUS_ABSENT for item in result)


def test_mixed_colors():
    target = "APPLE"
    guess = "ALERT"
    result = evaluate_guess(target, guess)
    assert result[0]["status"] == STATUS_CORRECT  # A


def test_duplicates_target_abby():
    target = "ABBEY"
    guess = "BARRY"
    result = evaluate_guess(target, guess)
    statuses = [r["status"] for r in result]
    assert statuses[0] == STATUS_PRESENT
    assert statuses[1] == STATUS_PRESENT
    assert statuses[2] == STATUS_ABSENT
    assert statuses[3] == STATUS_ABSENT
    assert statuses[4] == STATUS_CORRECT


def test_case_insensitive():
    target = "apple"
    guess = "Apple"
    result = evaluate_guess(target, guess)
    assert all(item["status"] == STATUS_CORRECT for item in result)


def test_double_letter_present_once():
    target = "GREAT"
    guess = "AGREE"
    result = evaluate_guess(target, guess)
    assert result[0]["status"] == STATUS_PRESENT
    assert result[1]["status"] == STATUS_PRESENT
    assert result[2]["status"] == STATUS_PRESENT
    assert result[3]["status"] == STATUS_PRESENT
    assert result[4]["status"] == STATUS_ABSENT
