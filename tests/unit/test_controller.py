from pytest import fixture, mark
from pytest_mock import MockerFixture
from unittest.mock import MagicMock, AsyncMock

from windows_time_sync.windows import WindowsController


@fixture
def controller():
    return WindowsController(
        provider=AsyncMock()
    )

@fixture
def set_system_time(mocker: MockerFixture):
    return mocker.patch('windows_time_sync.controller.SetSystemTime')


@mark.asyncio
async def test_is_calling_windows_setsystemtime_method(
    controller: WindowsController,
    set_system_time: MagicMock
):
    await controller.set_time('')
    set_system_time.assert_called_once()
    