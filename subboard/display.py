import datetime
import typing

from .match import Match
from .score import BasicScoreStringer


class Display(typing.Protocol):
    def update(self) -> None:
        ...


class TerminalDisplay(Display):
    def __init__(self):
        self._score_stringer = BasicScoreStringer()
        self._what = "clock"
        self._since = None

    def update(self, match: Match) -> None:
        now = datetime.datetime.now()
        if self._since is None:
            self._since = now
        elif (now - self._since).total_seconds() > 5:
            self._since = now
            self._what = "clock" if self._what == "score" else "score"

        now_str = str(now)
        if self._what == "clock":
            print(now_str + "]", format_remaining(match.clock.current()))
        elif self._what == "score":
            print(now_str + "]", self._score_stringer.to_string(match.score))


def format_remaining(value: float) -> str:
    if value >= 60:
        minutes = int(value / 60)
        seconds = int(value % 60)
        return f"{minutes:02d}:{seconds:02d}"

    return f"{value:02.02f}"
