from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Restaurant Picker"
    envrionment: str = "local"

    class Config:
        env_file = ".env"


settings = Settings()
