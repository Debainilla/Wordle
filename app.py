"Main Streamlit app for Wordle game."

import streamlit as st

from src.constants import (
    MAX_ATTEMPTS,
    STATUS_ABSENT,
    STATUS_CORRECT,
    STATUS_PRESENT,
    WORD_LENGTH,
)
from src.game_logic import evaluate_guess, is_correct_guess
from src.ui import render_grid, render_keyboard
from src.word_service import get_random_word, load_words


def _initialize_session_state() -> None:
    """Initialize Streamlit session state."""
    if "initialized" not in st.session_state:
        st.session_state.initialized = True
        _reset_game()


def _reset_game() -> None:
    """Reset game state for a new game."""
    words = load_words()
    if not words:
        words = ["APPLE"]

    target = get_random_word(words)
    st.session_state.target_word = target
    st.session_state.guesses: list[list[str]] = []
    st.session_state.evaluations: list[list[dict]] = []
    st.session_state.current_row = 0
    st.session_state.current_col = 0
    st.session_state.game_over = False
    st.session_state.game_result = None
    st.session_state.message = ""
    st.session_state.key_colors: dict[str, str] = {}


def _update_key_colors(evaluation: list[dict[str, str]]) -> None:
    """Update keyboard colors with best status for each letter."""
    for item in evaluation:
        letter = item["letter"].upper()
        status = item["status"]
        current = st.session_state.key_colors.get(letter)

        priority = {STATUS_CORRECT: 3, STATUS_PRESENT: 2, STATUS_ABSENT: 1}
        if current is None or priority.get(status, 0) > priority.get(current, 0):
            st.session_state.key_colors[letter] = status


def _process_guess(guess_str: str) -> None:
    """Process a submitted guess."""
    if st.session_state.game_over:
        return

    guess_str = guess_str.upper().strip()
    if len(guess_str) != WORD_LENGTH:
        st.session_state.message = f"Guess must be {WORD_LENGTH} letters"
        return

    if not guess_str.isalpha():
        st.session_state.message = "Guess must contain only letters"
        return

    guess_letters = list(guess_str)

    target = st.session_state.target_word
    evaluation = evaluate_guess(target, guess_str)

    st.session_state.guesses.append(guess_letters)
    st.session_state.evaluations.append(evaluation)
    _update_key_colors(evaluation)

    if is_correct_guess(evaluation):
        st.session_state.game_over = True
        st.session_state.game_result = "win"
        st.session_state.message = "You win! Congratulations!"
    elif len(st.session_state.guesses) >= MAX_ATTEMPTS:
        st.session_state.game_over = True
        st.session_state.game_result = "lose"
        st.session_state.message = f"Game over! The word was {target}"
    else:
        st.session_state.message = ""


def main() -> None:
    """Run main Streamlit app."""
    st.set_page_config(page_title="Wordle", page_icon="Ã°Å¸Å½Â¯", layout="centered")

    st.title("Wordle")
    st.markdown("Guess the 5-letter word in 6 attempts!")

    _initialize_session_state()

    render_grid(st.session_state.guesses, st.session_state.evaluations)

    col1, col2 = st.columns([3, 1])

    with col1:
        guess_input = st.text_input(
            "Enter your guess",
            key="guess_input",
            max_chars=WORD_LENGTH,
            placeholder=f"Enter {WORD_LENGTH} letters",
            disabled=st.session_state.game_over,
        )

    with col2:
        submit_btn = st.button(
            "Submit",
            key="submit_btn",
            use_container_width=True,
        )

    if submit_btn and guess_input:
        _process_guess(guess_input)

    if submit_btn:
        st.rerun()

    if st.session_state.message:
        st.info(st.session_state.message)

    st.markdown("---")
    render_keyboard(st.session_state.key_colors)

    if st.session_state.game_over and st.button(
        "Play Again", type="primary", use_container_width=True
    ):
        _reset_game()
        st.rerun()


if __name__ == "__main__":
    main()
