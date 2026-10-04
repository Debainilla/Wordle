"""Streamlit UI helpers for Wordle game."""

import streamlit as st

from src.constants import (
    COLOR_ABSENT,
    COLOR_CORRECT,
    COLOR_PRESENT,
    KEY_ABSENT,
    KEY_CORRECT,
    KEY_DEFAULT,
    KEY_PRESENT,
    KEYBOARD_LAYOUT,
    STATUS_ABSENT,
    STATUS_CORRECT,
    STATUS_PRESENT,
)


def get_status_color(status: str) -> str:
    """Get hex color for tile status."""
    if status == STATUS_CORRECT:
        return COLOR_CORRECT
    if status == STATUS_PRESENT:
        return COLOR_PRESENT
    return COLOR_ABSENT


def render_tile(letter: str, status: str = STATUS_ABSENT) -> None:
    """Render a single game tile."""
    color = get_status_color(status)
    text_color = "white"
    display_letter = letter if letter else "&nbsp;"

    st.markdown(
        f"""
        <div style="
            width: 60px;
            height: 60px;
            background-color: {color};
            color: {text_color};
            border: 2px solid {color};
            border-radius: 4px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 32px;
            font-weight: bold;
            text-transform: uppercase;
            margin: 2px auto;
        ">
            {display_letter}
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_grid(guesses: list[list[str]], evaluations: list[list[dict]]) -> None:
    """Render game grid (6 rows x 5 columns)."""
    from src.constants import MAX_ATTEMPTS

    for row in range(MAX_ATTEMPTS):
        cols = st.columns(5)
        if row < len(evaluations):
            eval_row = evaluations[row]
            guess_row = guesses[row] if row < len(guesses) else []
            for col_idx in range(5):
                with cols[col_idx]:
                    letter = guess_row[col_idx] if col_idx < len(guess_row) else ""
                    status = (
                        eval_row[col_idx]["status"]
                        if col_idx < len(eval_row)
                        else STATUS_ABSENT
                    )
                    render_tile(letter=letter, status=status)
        elif row < len(guesses):
            guess_row = guesses[row]
            for col_idx in range(5):
                with cols[col_idx]:
                    letter = guess_row[col_idx] if col_idx < len(guess_row) else ""
                    render_tile(letter=letter, status=STATUS_ABSENT)
        else:
            for col_idx in range(5):
                with cols[col_idx]:
                    render_tile(letter="", status=STATUS_ABSENT)


def get_key_color(key: str, key_colors: dict[str, str]) -> str:
    """Get background color for keyboard key."""
    if key in ("ENTER", "DELETE"):
        return KEY_DEFAULT

    key_upper = key.upper()
    status = key_colors.get(key_upper)
    if status == STATUS_CORRECT:
        return KEY_CORRECT
    if status == STATUS_PRESENT:
        return KEY_PRESENT
    if status == STATUS_ABSENT:
        return KEY_ABSENT
    return KEY_DEFAULT


def render_keyboard(key_colors: dict[str, str]) -> None:
    """Render virtual keyboard."""
    for row_keys in KEYBOARD_LAYOUT:
        cols = st.columns(len(row_keys))
        for idx, key in enumerate(row_keys):
            with cols[idx]:
                bg_color = get_key_color(key, key_colors)
                text_color = "black" if bg_color == KEY_DEFAULT else "white"
                border_color = "#c0c0c0" if bg_color == KEY_DEFAULT else bg_color

                st.markdown(
                    f"""
                    <div style="
                        height: 48px;
                        background-color: {bg_color};
                        color: {text_color};
                        border: 1px solid {border_color};
                        border-radius: 4px;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        font-size: 14px;
                        font-weight: bold;
                        user-select: none;
                    ">
                        {key}
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
