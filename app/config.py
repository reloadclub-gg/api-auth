from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    # App
    secret_key: str
    app_base_url: str
    tokens_algorithm: str = 'HS256'
    debug: bool = True
    session_expire_hours: int = 30
    steam_openid_url: str = 'https://steamcommunity.com/openid/login'
    steam_openid_lookup_field: str = 'openid.claimed_id'

    model_config = SettingsConfigDict(env_file='.env', extra='ignore')


settings = Settings()
