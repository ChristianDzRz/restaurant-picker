from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Restaurant Picker"
    environment: str = "local"

    # Database settings
    database_url: str = "sqlite+aiosqlite:///./restaurant_picker.db"
    database_echo: bool = False  # Set to True to see SQL queries in logs

    class Config:
        env_file = ".env"


settings = Settings()
