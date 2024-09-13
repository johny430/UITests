from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    user_agent_path: str
    driver_path: str
    proxy_path: str
    google_credentials_path: str
    google_sheet_credentials_path: str
    twitter_credentials_path: str
    openai_api_key: str
    two_captcha_api_key: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )


config = Settings()
