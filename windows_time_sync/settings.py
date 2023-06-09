from dataclasses import dataclass

@dataclass
class TimeApiSettings:
    host: str
    time_path: str

    def get_time_uri(self) -> str:
        return self.host + self.time_path
        