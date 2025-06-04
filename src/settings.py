from enum import Enum

from pydantic_settings import BaseSettings, SettingsConfigDict


class API_VERSION(str, Enum):
    V1 = "v1"


class Settings(BaseSettings):
    # Database settings
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: str = "5432"
    POSTGRES_DB: str = "api_omega"

    @property
    def DATABASE_URL(self) -> str:
        """Get database URL."""
        return (
            f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}"
            f"/{self.POSTGRES_DB}"
        )

    # API settings
    API_BASE_PATH: str = f"/api/{API_VERSION.V1}"
    PROJECT_NAME: str = "API Omega"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )


settings = Settings()
