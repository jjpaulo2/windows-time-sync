from datetime import datetime
from win32api import SetSystemTime

from windows_time_sync._protocols.provider import TimeProvider


class WindowsController:

    def __init__(self, provider: TimeProvider):
        self._provider = provider

    def _timezone_correction(self, now: datetime) -> datetime:
        """
        This corrections is necessary to turn the time definition
        more easy. Removing the necessity of set adicional timezone
        informations.

        When use the Windows api method `SetSystemTime`, the time
        is setten using UTC as reference.

        Therefore, if your timezone is America/Sao_Paulo (-3), and you
        set `21:00` as the time, your system will show `18:00`.
        """
        return now - now.utcoffset()

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

    async def get_timezones(self):
        return self._provider.timezones()

    async def set_time(self, timezone: str) -> None:
        now = await self._provider.now(timezone)
        fixed_now = self._timezone_correction(now)
        windows_time_tuple = self._get_windows_time_tuple(fixed_now)
        
        SetSystemTime(*windows_time_tuple)
