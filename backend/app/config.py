from pydantic_settings import SettingsConfigDict,BaseSettings

class Settings(BaseSettings):
    model_config=SettingsConfigDict(env_file=".env",extra="ignore")
    DB_PORT:int
    DB_USER:str
    DB_PASSWORD:str
    DB_NAME:str
    DB_HOST:str
    ACCESS_TOKEN_EXPIRE_MINUTES:int
    SECRET_KEY:str
    ALGORITHM:str
settings=Settings()
