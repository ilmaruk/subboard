# The following events are defined
# -- clock --
# KICK_OFF (duration: float[600]): starts a game of duration seconds
# PAUSE: pauses a game
# RESUME: resumes a game
# RESTART: starts a new period (e.g.: second half)
# STOP: stops a game (for ascending clocks only)
# -- score --
# SCORE (who: string, qty: int[1]): adds a goal to "who"
# AMEND (who: string, qty: int[1]): removes a goal from "who"

import enum
import json
import typing


class EventType(enum.StrEnum):
    KICK_OFF = "kick_off"
    PAUSE = "pause"
    RESUME = "resume"
    RESTART = "restart"
    STOP = "stop"
    SCORE = "score"
    AMEND = "amend"


class Event:
    def __init__(self, message: str) -> None:
        self.__dict__ = json.loads(message)

    @property
    def type(self) -> str:
        return self.__dict__.get("type")

    def __getattr__(self, key: str) -> typing.Any:
        return self.__dict__.get(key)


class KickOffEvent(Event):
    def __init__(self, message: str) -> None:
        super().__init__(message)

    @property
    def duration(self):
        return self.__dict__.get("duration", 600)


class ScoreEvent(Event):
    def __init__(self, message: str) -> None:
        super().__init__(message)

    @property
    def who(self):
        return self.__dict__.get("who")

    @property
    def qty(self):
        return self.__dict__.get("qty", 1)


def event_factory(message: str) -> typing.Optional[Event]:
    payload = json.loads(message)
    typ = payload.get("type")
    if typ is None:
        return None

    if typ == EventType.KICK_OFF:
        return KickOffEvent(message)
    elif typ == EventType.SCORE:
        return ScoreEvent(message)
    else:
        return Event(message)
