from datetime import datetime
from win32api import SetSystemTime

from windows_time_sync._protocols.provider import TimeProvider


class ApplyWindowsDatetime:

    def __init__(self, provider: TimeProvider):
        self.provider = provider

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
    
    async def apply(self) -> None:
        now = await self.provider.now()
        windows_time_tuple = self._get_windows_time_tuple(now)

        try:
            SetSystemTime(*windows_time_tuple)
            print(f'Windows current datetime set to {now} (UTC).')

        except Exception as exc:
            print('Error while tryied to update Windows time.')
            print(exc)
