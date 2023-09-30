from .clock import Clock
from .score import Score


class Match:
    def __init__(self, clock: Clock) -> None:
        self.status = "scheduled"
        self.clock = clock
        self.score = Score()

    def start(self, duration: int) -> None:
        self.status = "started"
        self.clock.start(duration)

    def goal(self, who: str) -> None:
        self.score.goal(who)
