from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    PROJECT_NAME: str = "BridgePoint"

    # Telegram Configuration
    TELEGRAM_BOT_TOKEN: str
    TELEGRAM_CHAT_ID: str

    # Database Configuration (Placeholder)
    DATABASE_URL: str

    # Timezone Configuration
    APP_TIMEZONE: str = "UTC"


settings = Settings()
