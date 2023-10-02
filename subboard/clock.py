from datetime import datetime
import typing


class Clock(typing.Protocol):
    def start(self, duration: int) -> None:
        """Starts a new period, of length 'duration' seconds.
        """
        ...

    def restart(self) -> None:
        """Like start(), but with an already known duration.
        """
        ...

    def pause(self) -> None:
        ...

    def resume(self) -> None:
        ...

    def stop(self) -> None:
        ...

    def running(self) -> bool:
        """Tells whether the clock is running or not.
        """
        ...

    def current(self, now=None) -> float:
        ...


class DescendingClock(Clock):
    def __init__(self) -> None:
        super().__init__()
        self._duration = 0
        self._started_at = None
        self._spent = 0

    def start(self, duration: int) -> None:
        if self.running():
            # already running
            return None  # todo: raise errors

        self._duration = duration
        return self.restart()

    def restart(self) -> None:
        if self.running():
            # already running
            return None

        self._spent = 0
        self._started_at = datetime.now()

    def pause(self) -> None:
        if not self.running():
            # Not running
            return None

        self._spent += (datetime.now() - self._started_at).total_seconds()
        self._started_at = None

    def resume(self) -> None:
        if self.running():
            # already running
            return None

        self._started_at = datetime.now()

    def stop(self) -> None:
        """Not required with this clock.
        """
        self._spent = 0
        return self.pause()

    def running(self) -> bool:
        return self._started_at is not None

    def current(self, now=None) -> float:
        """Returns the number of seconds till the end.
        """
        if self.running():
            spent = (datetime.now() -
                     self._started_at).total_seconds() + self._spent
        else:
            # Not running, hence returning the time spent till the pause
            spent = self._spent
        return self._duration - spent
