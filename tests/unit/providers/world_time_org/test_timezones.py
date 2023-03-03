from pytest import mark, fixture
from unittest.mock import AsyncMock, MagicMock
from json import JSONDecodeError

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
def http_client_empty():
    http_response_json_mock = MagicMock(
        return_value=[]
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
def http_client_json_error():
    http_response_json_mock = MagicMock(
        side_effect=JSONDecodeError('', '', 0)
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

@fixture
def provider_empty(settings: TimeApiSettings, http_client_empty: AsyncMock):
    return WorldTimeOrgProvider(
        settings=settings,
        http_client=http_client_empty
    )

@fixture
def provider_json_error(settings: TimeApiSettings, http_client_json_error: AsyncMock):
    return WorldTimeOrgProvider(
        settings=settings,
        http_client=http_client_json_error
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

@mark.asyncio
async def test_get_timezones_returns_empty(provider_empty: WorldTimeOrgProvider):
    response = await provider_empty.timezones()
    assert len(response) == 0

@mark.asyncio
async def test_get_timezones_json_error(provider_json_error: WorldTimeOrgProvider):
    response = await provider_json_error.timezones()
    assert response == None
