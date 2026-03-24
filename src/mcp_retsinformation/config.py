from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    retsinformation_base_url: str = "https://retsinformation-api.dk"

    model_config = {"env_file": ".env"}


settings = Settings()
