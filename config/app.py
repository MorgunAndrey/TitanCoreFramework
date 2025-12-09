# config/app.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_base_name: str = "TitanCore"
    debug: bool = False
    environment: str = "development"
    timezone: str = "UTC"
    
    app_base_url: str = "http://localhost:8000"
    mail_mailer: str = "smtp"
    mail_from_name: str = "TitanCore Framework"

    # Настройки БД
    database_user: str = "root"
    database_password: str = ""
    database_host: str = "localhost"
    database_port: int = 3306
    database_name: str = "test_db"

    # Настройки почты
    mail_host: str = "smtp.mail.ru"
    mail_port: int = 465
    mail_username: str = ""
    mail_password: str = ""
    mail_encryption: str = ""
    mail_from_address: str = ""

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore" 

settings = Settings()