from httpx import AsyncClient

from windows_time_sync.windows import ApplyWindowsDatetime
from windows_time_sync.settings import TimeApiSettings
from windows_time_sync.providers.world_time_org import WorldTimeOrgProvider


settings = TimeApiSettings(
    host='http://worldtimeapi.org',
    time_path='/api/timezone/Etc/UTC'
)

async def main() -> None:
    async with AsyncClient() as http_client:
        provider = WorldTimeOrgProvider(settings, http_client)
        windows_datetime = ApplyWindowsDatetime(provider)
        await windows_datetime.apply()
