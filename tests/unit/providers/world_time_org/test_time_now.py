from pytest import mark, fixture
from unittest.mock import AsyncMock, MagicMock
from datetime import datetime
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
def time_now_response():
    return {
        "datetime": "2023-02-28T00:21:12.929762+00:00"
    }

@fixture
def http_client_success(time_now_response: dict[str, str]):
    http_response_json_mock = MagicMock(
        return_value=time_now_response
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
        return_value={}
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
def provider_none(settings: TimeApiSettings, http_client_empty: AsyncMock):
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
async def test_get_time_now_returns_datetime(provider_success: WorldTimeOrgProvider):
    response = await provider_success.now('')
    assert type(response) == datetime

@mark.asyncio
async def test_get_time_now_returns_none(provider_none: WorldTimeOrgProvider):
    response = await provider_none.now('')
    assert response == None

@mark.asyncio
async def test_get_time_now_json_error(provider_json_error: WorldTimeOrgProvider):
    response = await provider_json_error.now('')
    assert response == None
