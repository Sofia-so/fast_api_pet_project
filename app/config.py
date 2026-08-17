from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_uri: str
    test_database_uri: str

    model_config = SettingsConfigDict(
        env_file=".env",
    )


settings = Settings()
