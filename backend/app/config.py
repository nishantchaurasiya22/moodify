from pydantic_settings import BaseSettings,SettingsConfigDict
class Settings(BaseSettings):
    model_config=SettingsConfigDict(env_file=".env",extra="ignore")
    DB_PORT:int
    DB_USER:str
    DB_PASSWORD:str
    DB_NAME:str
    DB_HOST:str
    SECRET_KEY:str
    ACCESS_TOKEN_EXPIRE_MINUTES:int
    ALGORITHM:str
settings=Settings()

