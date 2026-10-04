"""Constants for Wordle game."""

WORD_LENGTH = 5
MAX_ATTEMPTS = 6

# Tile statuses
STATUS_CORRECT = "correct"  # Green
STATUS_PRESENT = "present"  # Yellow
STATUS_ABSENT = "absent"  # Gray

# Display colors (hex) for tiles
COLOR_CORRECT = "#6aaa64"
COLOR_PRESENT = "#c9b458"
COLOR_ABSENT = "#787c7e"

# Keyboard colors
KEY_DEFAULT = "#d3d6da"
KEY_CORRECT = COLOR_CORRECT
KEY_PRESENT = COLOR_PRESENT
KEY_ABSENT = COLOR_ABSENT

# QWERTY keyboard layout (rows)
KEYBOARD_LAYOUT = [
    ["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
    ["A", "S", "D", "F", "G", "H", "J", "K", "L"],
    ["ENTER", "Z", "X", "C", "V", "B", "N", "M", "DELETE"],
]
