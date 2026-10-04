# Wordle in Streamlit

A simple Wordle game built with Streamlit, following PEP8 and best practices.

## Setup

`ash
pip install -r requirements.txt
`

## Run

`ash
streamlit run app.py
`

## Tests

`ash
pytest
`

## Lint & Format

`ash
ruff check .
ruff format .
`

## Rules

- 6 attempts to guess a 5-letter word
- Green: correct letter, correct position
- Yellow: correct letter, wrong position
- Gray: letter not in word
