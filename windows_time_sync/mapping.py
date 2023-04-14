from pydantic import BaseSettings

from windows_time_sync._protocols.http_client import HttpClient
from windows_time_sync._protocols.provider import TimeProvider
from windows_time_sync.providers.world_time_org import WorldTimeOrgProvider


_PROVIDERS = {
    'WorldTime.org': WorldTimeOrgProvider
}


def get_provider(name: str, settings: BaseSettings, http_client: HttpClient) -> TimeProvider:
    return _PROVIDERS[name](settings, http_client)
    
def get_providers_list() -> list[str]:
    return list(_PROVIDERS.keys())
    