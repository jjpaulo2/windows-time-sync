from pydantic import BaseSettings, Field


class TimeApiSettings(BaseSettings):
    host: str = Field(env='TIME_API_HOST')
    timezones_path: str = Field(env='TIME_API_TIMEZONES_PATH')
    time_path: str = Field(env='TIME_API_TIME_PATH')

    def get_timezones_uri(self) -> str:
        return self.host + self.timezones_path

    def get_time_uri(self, timezone: str) -> str:
        time_path_with_timezone = self.time_path.format(
            timezone=timezone
        )
        return self.host + time_path_with_timezone
        