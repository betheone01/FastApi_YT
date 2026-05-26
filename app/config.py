from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    HOST: str
    DB_PORT: str
    PASSWORD: str = "ani@9355"
    DATABASE: str
    DB_USER: str = "postgres"
    ALGORITHM: str
    SECRET_KEY: str = "11557357bb6e0cc1f0f0cce87d377332d44966ba12dc96f348691cd6e6903481"
    ACCESS_TOKEN_EXPIRE_MINUTES: str

    class Config:
        env_file = ".env"

settings = Settings()

