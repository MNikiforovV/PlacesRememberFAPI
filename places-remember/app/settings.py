from pydantic import BaseSettings


class Settings(BaseSettings):
    secret_key: str
    google_client_id: str
    google_client_secret: str

    class Config:
        env_file = ".env"
