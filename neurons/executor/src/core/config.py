from typing import Optional
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    PROJECT_NAME: str = "compute-subnet-executor"

    INTERNAL_PORT: int = Field(env="INTERNAL_PORT", default=8001)
    SSH_PORT: int = Field(env="SSH_PORT", default=22)

    MINER_HOTKEY_SS58_ADDRESS: str = Field(env="MINER_HOTKEY_SS58_ADDRESS")

    RENTING_PORT_RANGE: Optional[str] = Field(env="RENTING_PORT_RANGE", default=None)
    RENTING_PORT_MAPPINGS: Optional[str] = Field(env="RENTING_PORT_MAPPINGS", default=None)
    COMPUTE_APP_URI: str = "wss://celiumcompute.ai"

    ENV: str = Field(env="ENV", default="dev")


settings = Settings()
