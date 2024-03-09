from __future__ import annotations

from typing import Protocol


class HttpResponse(Protocol):

    def json(self) -> dict[str, str] | list[str]:
        pass


class HttpClient(Protocol):

    async def get(self, url: str, *args, **kwargs) -> HttpResponse:
        pass
