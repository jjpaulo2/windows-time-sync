from __future__ import annotations

from typing import Self
from datetime import datetime
from contextlib import suppress
from json import JSONDecodeError
from httpx import TimeoutException

from windows_time_sync._protocols.http_client import HttpClient
from windows_time_sync.settings import TimeApiSettings


class WorldTimeOrgProvider:
    """
    Provider from World Time API.
    See more at http://worldtimeapi.org/
    """

    _EXCEPTIONS_TO_SUPRESS = (
        JSONDecodeError,
        TimeoutException,
    )

    def __init__(self, settings: TimeApiSettings, http_client: HttpClient) -> Self:
        self._settings = settings
        self._http_client = http_client

    async def _http_request(self, uri: str) -> list[str] | dict[str, str] | None:
        response_formatted = None

        with suppress(*self._EXCEPTIONS_TO_SUPRESS):
            response = await self._http_client.get(uri)
            response_formatted = response.json()

        return response_formatted

    async def timezones(self) -> list[str] | None:
        return await self._http_request(
            uri=self._settings.get_timezones_uri()
        )

    async def now(self, timezone: str) -> datetime | None:
        response_dict = await self._http_request(
            uri=self._settings.get_time_uri(timezone)
        )

        if isinstance(response_dict, dict):
            datetime_string = response_dict.get('datetime')

            if datetime_string:
                return datetime.fromisoformat(datetime_string)

        return None
        