# config/app.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Основные настройки
    appBaseName: str = "FastAPI Laravel Clone"
    debug: bool = False
    environment: str = "production"
    timezone: str = "UTC"
    
    appBaseUrl: str = "http://localhost:8000"
    mailMailer: str = "smtp"
    mailFromName: str = "TitanCore Framework"

    # Настройки БД
    databaseUser: str = "root"
    databasePassword: str = ""
    databaseHost: str = "localhost"
    databasePort: int = 3306
    databaseName: str = "test_db"

    # Настройки почты
    mailHost: str = "smtp.mail.ru"
    mailPort: int = 465
    mailUsername: str = ""
    mailPassword: str = ""
    mailEncryption: str = ""
    mailFromAddress: str = ""

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore" 

settings = Settings()