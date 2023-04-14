from datetime import datetime

from win32api import SetSystemTime
from pydantic import BaseSettings

from windows_time_sync._protocols.provider import TimeProvider
from windows_time_sync._protocols.http_client import HttpClient
from windows_time_sync.mapping import get_provider


class WindowsController:

    def __init__(self, settings: BaseSettings, http_client: HttpClient):
        self.settings = settings
        self.http_client = http_client

    def _get_windows_time_tuple(self, now: datetime) -> tuple:
        return (
            now.year,
            now.month,
            now.weekday(),
            now.day,
            now.hour,
            now.minute,
            now.second,
            int(now.microsecond * 0.001)
        )

    async def apply_datetime(self, provider_name: str) -> None:
        provider = get_provider(
            provider_name,
            self.settings,
            self.http_client
        )
        windows_time_tuple = self._get_windows_time_tuple(
            now=await provider.now()
        )
        
        SetSystemTime(*windows_time_tuple)
