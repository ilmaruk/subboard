from .match import Match
from .score import BasicScoreStringer


def format_remaining(value: int) -> str:
    minutes = int(value / 60)
    seconds = int(value % 60)
    return f"{minutes:02d}:{seconds:02d}"
