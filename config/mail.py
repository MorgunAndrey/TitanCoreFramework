# config/mail.py
from dotenv import load_dotenv
import os

load_dotenv()

def get_env_str(key: str, default: str = "") -> str:
    """Безопасное получение строковой переменной окружения"""
    value = os.getenv(key, default)
    return str(value) if value is not None else default

def get_env_int(key: str, default: int = 0) -> int:
    """Безопасное получение целочисленной переменной окружения"""
    value = os.getenv(key)
    try:
        return int(value) if value is not None else default
    except (ValueError, TypeError):
        return default

def get_env_bool(key: str, default: bool = False) -> bool:
    """Безопасное получение булевой переменной окружения"""
    value = os.getenv(key)
    if value is None:
        return default
    return value.lower() in ('true', '1', 'yes', 'y', 't')

# Настройки SMTP с гарантированными типами
mailHost = get_env_str("mail_host", "smtp.mail.ru")
mailPort = get_env_int("mail_port", 465)
mailUsername = get_env_str("mail_username", "")
mailPassword = get_env_str("mail_password", "")
mailEncryption = get_env_str("mail_encryption", "ssl")
mailFromAddress = get_env_str("mail_from_address", "")
mailFromName = get_env_str("mail_from_name", get_env_str("mail_from_name", "TitanCore Framework"))

# URL приложения
appBaseUrl = get_env_str("app_base_url", "http://localhost:8000")
appBaseName = get_env_str("app_base_name", "TitanCore Framework")



