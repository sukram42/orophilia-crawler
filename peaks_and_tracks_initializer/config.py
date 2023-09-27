from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

class Configurations(BaseSettings):
    model_config = SettingsConfigDict(env_nested_delimiter='__')


@lru_cache()
def get_configuration():
    return Configurations()