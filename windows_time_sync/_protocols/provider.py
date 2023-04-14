from __future__ import annotations

from typing import Protocol
from datetime import datetime


class TimeProvider(Protocol):

    async def now(self) -> datetime:
        "Must return now as UTC time."
