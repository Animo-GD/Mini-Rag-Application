from pydantic_settings import BaseSettings,SettingsConfigDict

class Setting(BaseSettings):
    APP_NAME:str
    APP_VERSION:str
    OPENROUTER_API_KEY:str
    FILE_ALLOWED_TYPES:list
    FILE_MAX_SIZE:int
    FILE_DEFAULT_CHUNK_SIZE:int
    class Config:
        env_file=".env"

def get_settings():
    return Setting()