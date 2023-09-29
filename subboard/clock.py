from datetime import datetime


class Clock:
    def __init__(self) -> None:
        self._duration = 0
        self._started_at = 0

    def start(self, duration: int) -> None:
        self._duration = duration
        self._started_at = datetime.now()

    def value(self, now=None) -> float:
        """Returns the number of seconds till the end.
        """
        if now is None:
            now = datetime.now()

        value = self._duration - (now - self._started_at).total_seconds()
        return value if value > 0 else 0
