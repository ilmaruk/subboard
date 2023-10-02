# States for the state-machine
from abc import ABC
import enum

from .events import Event, EventType
from .match import Match


class States(enum.StrEnum):
    BEFORE_MATCH = "BeforeMatch"
    DURING_MATCH = "DuringMatch"
    PAUSED_MATCH = "PausedMatch"
    AFTER_MATCH = "AfterMatch"


class State(ABC):
    def __init__(self, match: Match) -> None:
        self._match = match

    def process_event(self, event: Event) -> "State":
        ...


class PausedMatchState(State):
    type = States.PAUSED_MATCH

    def __init__(self, match: Match) -> None:
        super().__init__(match)

    def process_event(self, event: Event) -> State:
        if event.type != EventType.RESUME:
            # Invalid state
            return self

        self._match.clock.resume()

        return DuringMatchState(self._match)


class AfterMatchState(State):
    type = States.AFTER_MATCH

    def __init__(self, match: Match) -> None:
        super().__init__(match)

    def process_event(self, event: Event) -> State:
        if event.type != EventType.RESTART:
            # Invalid state
            return self

        return DuringMatchState(self._match)


class DuringMatchState(State):
    type = States.DURING_MATCH

    def __init__(self, match: Match) -> None:
        super().__init__(match)

    def process_event(self, event: Event) -> State:
        if event.type == EventType.PAUSE:
            self._match.clock.pause()
            return PausedMatchState(self._match)
        elif event.type == EventType.STOP:
            self._match.clock.stop()
            return AfterMatchState(self._match)

        if event.type == EventType.SCORE:
            self._match.goal(event.who)
        elif event.type == EventType.AMEND:
            pass

        # Stay in the same state
        return self


class BeforeMatchState(State):
    type = States.BEFORE_MATCH

    def __init__(self, match: Match) -> None:
        super().__init__(match)

    def process_event(self, event: Event) -> State:
        if event.type != EventType.KICK_OFF:
            # Invalid state
            return self

        self._match.start(event.duration)

        return DuringMatchState(self._match)
