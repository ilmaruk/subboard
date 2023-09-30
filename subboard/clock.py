from datetime import datetime
import typing


class Clock(typing.Protocol):
    def start(self, duration: int) -> None:
        ...

    def restart(self) -> None:
        ...

    def pause(self) -> float:
        ...

    def resume(self) -> float:
        ...

    def stop(self) -> float:
        ...

    def current(self, now=None) -> float:
        ...


class DescendingClock(Clock):
    def __init__(self) -> None:
        super().__init__()
        self._duration = 0
        self._started_at = 0
        self._pause_started_at = None
        self._offset = 0

    def start(self, duration: int) -> None:
        self._duration = duration
        self._started_at = datetime.now()

    def restart(self) -> None:
        pass  # for now ...

    def pause(self) -> None:
        if self._pause_started_at is not None:
            # Already paused
            return

        self._pause_started_at = datetime.now()

    def resume(self) -> None:
        if self._pause_started_at is None:
            # Not paused
            return

        self._offset += (datetime.now() -
                         self._pause_started_at).total_seconds()
        self._pause_started_at = None

    def stop(self) -> None:
        """Not required with this clock.
        """
        pass

    def current(self, now=None) -> float:
        """Returns the number of seconds till the end.
        """
        if now is None:
            now = datetime.now()

        value = self._duration - \
            (now - self._started_at - self._offset).total_seconds()
        return value if value > 0 else 0
