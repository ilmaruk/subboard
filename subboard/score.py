import typing


class Score:
    def __init__(self):
        self.score = {
            "home": 0,
            "away": 0,
        }

    def goal(self, who: str) -> None:
        self.score[who] += 1


class ScoreStringer(typing.Protocol):
    def to_string(self, score: Score) -> str:
        ...


class BasicScoreStringer(ScoreStringer):
    def to_string(self, score: Score) -> str:
        return f"{score.score['home']}-{score.score['away']}"
