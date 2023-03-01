from pytest import mark, fixture
from unittest.mock import AsyncMock, MagicMock

from windows_time_sync.providers.world_time_org import WorldTimeOrgProvider
from windows_time_sync.settings import TimeApiSettings


@fixture
def settings():
    return TimeApiSettings(
        host='',
        timezones_path='',
        time_path=''
    )

@fixture
def timezones_response():
    return [
        "Region1/Country1",
        "Region1/Country2",
        "Region2/Country1",
        "Region2/Country2"
    ]

@fixture
def http_client_success(timezones_response: list[str]):
    http_response_json_mock = MagicMock(
        return_value=timezones_response
    )
    http_response_mock = MagicMock(
        json=http_response_json_mock
    )
    http_client_get = AsyncMock(
        return_value=http_response_mock
    )
    return AsyncMock(
        get=http_client_get
    )

@fixture
def provider_success(settings: TimeApiSettings, http_client_success: AsyncMock):
    return WorldTimeOrgProvider(
        settings=settings,
        http_client=http_client_success
    )


@mark.asyncio
async def test_get_timezones_returns_list(provider_success: WorldTimeOrgProvider):
    response = await provider_success.timezones()
    assert type(response) == list

@mark.asyncio
async def test_get_timezones_returns_list_of_string(provider_success: WorldTimeOrgProvider):
    response = await provider_success.timezones()
    first_element = response[0]
    assert type(first_element) == str
