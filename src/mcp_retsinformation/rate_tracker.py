import time
from dataclasses import dataclass, field


@dataclass
class RateTracker:
    """Tracks API request counts against retsinformation-api.dk rate limits (20/hour, 50/day)."""

    max_per_hour: int = 20
    max_per_day: int = 50
    _timestamps: list[float] = field(default_factory=list)

    def record(self) -> None:
        self._timestamps.append(time.time())

    def _count_since(self, seconds_ago: float) -> int:
        cutoff = time.time() - seconds_ago
        return sum(1 for ts in self._timestamps if ts > cutoff)

    @property
    def requests_last_hour(self) -> int:
        return self._count_since(3600)

    @property
    def requests_last_day(self) -> int:
        return self._count_since(86400)

    @property
    def remaining_hour(self) -> int:
        return max(0, self.max_per_hour - self.requests_last_hour)

    @property
    def remaining_day(self) -> int:
        return max(0, self.max_per_day - self.requests_last_day)

    def status(self) -> dict:
        return {
            "requests_last_hour": self.requests_last_hour,
            "requests_last_day": self.requests_last_day,
            "remaining_hour": self.remaining_hour,
            "remaining_day": self.remaining_day,
            "limit_hour": self.max_per_hour,
            "limit_day": self.max_per_day,
        }


tracker = RateTracker()
