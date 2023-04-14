from asyncio import new_event_loop
from httpx import AsyncClient

import PySimpleGUI as sg

from windows_time_sync.controller import WindowsController
from windows_time_sync.settings import TimeApiSettings
from windows_time_sync.mapping import get_providers_list


def get_window(providers: list[str]):
    sg.theme('DarkAmber')
    layout = [
        [sg.Text('Select your provider:')],
        [sg.Listbox(providers, size=(100, 10))],
        [sg.Button('Apply', size=(100, 2))],
    ]
    return sg.Window('Windows Time Sync', layout, size=(300, 280))


async def window_loop(window: sg.Window, controller: WindowsController):
    while True:
        event, values = window.read()
        
        if event == sg.WIN_CLOSED:
            break

        if event == 'Apply':
            await controller.apply_datetime(values[0][0])

    window.close()


async def main():
    settings = TimeApiSettings(
        host='http://worldtimeapi.org',
        time_path='/api/timezone/Etc/UTC'
    )

    async with AsyncClient() as http_client:
        providers_list = get_providers_list()
        controller = WindowsController(
            settings,
            http_client
        )
        
        await window_loop(
            get_window(providers_list),
            controller
        )


if __name__ == '__main__':
    loop = new_event_loop()
    now = loop.run_until_complete(main())
