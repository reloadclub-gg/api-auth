from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    # App
    secret_key: str
    tokens_algorithm: str = 'HS256'
    debug: bool = True
    session_expire_hours: int = 30

    model_config = SettingsConfigDict(env_file='.env', extra='ignore')


settings = Settings()
