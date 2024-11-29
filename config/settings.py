from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    database_url: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int


settings = Settings()  # type: ignore

print(settings.database_url)
print(settings.secret_key)
print(settings.algorithm)
print(settings.access_token_expire_minutes)
