from pydantic import BaseSettings, Field


class TimeApiSettings(BaseSettings):
    host: str = Field(env='TIME_API_HOST')
    time_path: str = Field(env='TIME_API_TIME_PATH')

    def get_time_uri(self) -> str:
        return self.host + self.time_path
        