from pytest import fixture, mark
from pytest_mock import MockerFixture
from unittest.mock import MagicMock, AsyncMock

from windows_time_sync.windows import ApplyWindowsDatetime


@fixture
def windows_datetime():
    return ApplyWindowsDatetime(
        provider=AsyncMock()
    )

@fixture
def set_system_time(mocker: MockerFixture):
    return mocker.patch('windows_time_sync.windows.SetSystemTime')


@mark.asyncio
async def test_is_calling_windows_setsystemtime_method(
    windows_datetime: ApplyWindowsDatetime,
    set_system_time: MagicMock
):
    await windows_datetime.apply()
    set_system_time.assert_called_once()
    