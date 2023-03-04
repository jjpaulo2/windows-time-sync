from asyncio import new_event_loop
from httpx import AsyncClient

import PySimpleGUI as sg

from windows_time_sync.providers.world_time_org import WorldTimeOrgProvider
from windows_time_sync.controller import WindowsController
from windows_time_sync.settings import TimeApiSettings


def get_window(timezones):
    sg.theme('DarkAmber')
    layout = [
        [sg.Text('Select your timezone:')],
        [sg.Listbox(timezones, size=(100, 10))],
        [sg.Button('Apply', size=(100, 2))],
    ]
    return sg.Window('Windows Time Sync', layout, size=(300, 280))


async def window_loop(window: sg.Window, controller: WindowsController):
    while True:
        event, values = window.read()
        
        if event == sg.WIN_CLOSED:
            break

        if event == 'Apply':
            await controller.set_time(values[0][0])

    window.close()


async def main():
    settings = TimeApiSettings(
        host='http://worldtimeapi.org',
        timezones_path='/api/timezone',
        time_path='/api/timezone/{timezone}'
    )

    async with AsyncClient() as http_client:
        provider = WorldTimeOrgProvider(settings, http_client)
        controller = WindowsController(provider)
        timezones = await controller.get_timezones()
        print(timezones)
        await window_loop(get_window(timezones), controller)


if __name__ == '__main__':
    loop = new_event_loop()
    now = loop.run_until_complete(main())
