from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class ConfigBase(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


class BrowserConfig(ConfigBase):
    model_config = SettingsConfigDict(env_prefix="BROWSER_")

    NAME: str = "chrome"
    OPTIONS_CHROME: str = "--window-size=1920,1080"
    OPTIONS_FIREFOX: str = "--window-size=1920,1080"
    OPTIONS_EDGE: str = "--window-size=1920,1080"


class TheInternetConfig(ConfigBase):
    model_config = SettingsConfigDict(env_prefix="THE_INTERNET_")
    HOST: str
    PORT: int

    @property
    def base_url(self) -> str:
        return f"http://{self.HOST}:{self.PORT}"
    
    @property
    def basic_auth_url(self) -> str:
        return f"http://admin:admin@{self.HOST}:{self.PORT}/basic_auth"


class Config(BaseSettings):
    browser: BrowserConfig = Field(default_factory=BrowserConfig)
    the_internet: TheInternetConfig = Field(default_factory=TheInternetConfig)

    @classmethod
    def load(cls) -> "Config":
        return cls()