from __future__ import annotations

from typing import Protocol
from datetime import datetime


class TimeProvider(Protocol):

    async def timezones(self) -> list[str]:
        pass

    async def now(self, timezone: str) -> datetime:
        pass
