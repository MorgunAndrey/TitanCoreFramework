import time
from typing import Dict, Tuple


class RateLimitService:
    """Simple in-memory rate limiter for per-key throttling."""

    _attempts: Dict[str, Tuple[int, float]] = {}

    @classmethod
    def check_and_increment(cls, key: str, limit: int, window_seconds: int) -> bool:
        """Returns True if within limit; increments attempt counter."""
        now = time.time()
        attempts, window_start = cls._attempts.get(key, (0, now))

        # Reset window if expired
        if now - window_start >= window_seconds:
            attempts = 0
            window_start = now

        attempts += 1
        cls._attempts[key] = (attempts, window_start)

        return attempts <= limit

