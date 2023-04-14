from asyncio import new_event_loop
from sys import argv
from httpx import AsyncClient

from windows_time_sync.providers.world_time_org import WorldTimeOrgProvider
from windows_time_sync.controller import WindowsController
from windows_time_sync.settings import TimeApiSettings


async def main():
    settings = TimeApiSettings(
        host='http://worldtimeapi.org',
        timezones_path='/api/timezone',
        time_path='/api/timezone/{timezone}'
    )

    async with AsyncClient() as http_client:
        provider = WorldTimeOrgProvider(settings, http_client)
        controller = WindowsController(provider)
        await controller.set_time(argv[1])


if __name__ == '__main__':
    loop = new_event_loop()
    now = loop.run_until_complete(main())
