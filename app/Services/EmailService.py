# app/Services/EmailService.py
import smtplib
import ssl
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional
from config.mail import (
    mailHost, mailPort, mailUsername, mailPassword, 
    mailEncryption, mailFromAddress, mailFromName,
    appBaseUrl, appBaseName
)

logger = logging.getLogger(__name__)


class EmailService:
    
    @staticmethod
    def _validate_smtp_connection() -> bool:
        """Проверка валидности SMTP настроек"""
        if not all([mailHost, mailPort, mailUsername, mailPassword]):
            raise ValueError("Не все SMTP настройки заполнены")
        
        if not isinstance(mailHost, str) or not mailHost:
            raise ValueError("mailHost должен быть непустой строкой")
        
        if not isinstance(mailPort, int) or mailPort <= 0:
            raise ValueError("mailPort должен быть положительным числом")
            
        return True

    @staticmethod
    def send_password_reset_email(email: str, reset_token: str) -> bool:
        """Отправка email с ссылкой для сброса пароля"""
        try:
            # Проверяем настройки
            EmailService._validate_smtp_connection()
            
            # Генерация ссылки
            reset_url = f"{appBaseUrl}/password/reset/{reset_token}"
            
            # Создание сообщения
            msg = MIMEMultipart()
            msg['From'] = f"{mailFromName} <{mailFromAddress}>"
            msg['To'] = email
            msg['Subject'] = f"Сброс пароля - {appBaseName}"
            
            # HTML содержимое
            html_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="utf-8">
                <title>Сброс пароля</title>
            </head>
            <body>
                <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
                    <h2>Сброс пароля</h2>
                    <p>Вы получили это письмо, потому что запросили сброс пароля для вашей учетной записи.</p>
                    <p>Для сброса пароля перейдите по ссылке ниже:</p>
                    <p>
                        <a href="{reset_url}" style="background-color: #007bff; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; display: inline-block;">
                            Сбросить пароль
                        </a>
                    </p>
                    <p>Ссылка действительна в течение 1 часа.</p>
                    <p>Если вы не запрашивали сброс пароля, проигнорируйте это письмо.</p>
                    <hr>
                    <p>С уважением,<br>Команда {appBaseName}</p>
                </div>
            </body>
            </html>
            """
            
            msg.attach(MIMEText(html_content, 'html'))
            
            # Явное преобразование типов для TypeScript
            host = str(mailHost)
            port = int(mailPort)
            username = str(mailUsername)
            password = str(mailPassword)
            
            # Отправка через SMTP с SSL
            if mailEncryption == "ssl":
                context = ssl.create_default_context()
                with smtplib.SMTP_SSL(host, port, context=context) as server:
                    server.login(username, password)
                    server.send_message(msg)
            else:
                # Для TLS
                with smtplib.SMTP(host, port) as server:
                    if mailEncryption == "tls":
                        server.starttls()
                    server.login(username, password)
                    server.send_message(msg)
                
            return True
            
        except Exception as e:
            logger.error(f"Ошибка отправки email: {e}", exc_info=True)
            return False

    @staticmethod
    def test_connection() -> bool:
        """Тестирование подключения к SMTP серверу"""
        try:
            # Проверяем настройки
            EmailService._validate_smtp_connection()
            
            print(f"Попытка подключения к {mailHost}:{mailPort} с шифрованием {mailEncryption}...")
            
            # Явное преобразование типов
            host = str(mailHost)
            port = int(mailPort)
            username = str(mailUsername)
            password = str(mailPassword)
            
            if mailEncryption == "ssl":
                context = ssl.create_default_context()
                with smtplib.SMTP_SSL(host, port, context=context) as server:
                    print("SSL соединение установлено, attempting login...")
                    server.login(username, password)
                    print("SMTP подключение успешно (SSL)")
                    return True
            else:
                with smtplib.SMTP(host, port) as server:
                    if mailEncryption == "tls":
                        print("Starting TLS...")
                        server.starttls()
                    print("Attempting login...")
                    server.login(username, password)
                    print("SMTP подключение успешно (TLS)")
                    return True
                    
        except ValueError as e:
            logger.error(f"Ошибка конфигурации SMTP: {e}")
            return False
        except smtplib.SMTPAuthenticationError:
            logger.error("Ошибка аутентификации: неверный логин или пароль")
            return False
        except smtplib.SMTPConnectError:
            logger.error("Ошибка подключения к SMTP серверу")
            return False
        except smtplib.SMTPException as e:
            logger.error(f"Ошибка SMTP: {e}")
            return False
        except Exception as e:
            logger.error(f"Общая ошибка подключения к SMTP: {e}", exc_info=True)
            return False

    # Аналогично обновите send_welcome_email и send_test_email
    @staticmethod
    def send_welcome_email(email: str, username: str) -> bool:
        """Отправка приветственного email"""
        try:
            EmailService._validate_smtp_connection()
            
            msg = MIMEMultipart()
            msg['From'] = f"{mailFromName} <{mailFromAddress}>"
            msg['To'] = email
            msg['Subject'] = f"Добро пожаловать в {appBaseName}!"
            
            html_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="utf-8">
                <title>Добро пожаловать</title>
            </head>
            <body>
                <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
                    <h2>Добро пожаловать, {username}!</h2>
                    <p>Спасибо за регистрацию в {appBaseName}.</p>
                    <p>Теперь вы можете войти в свою учетную запись и начать использовать все возможности нашего фреймворка.</p>
                    <hr>
                    <p>С уважением,<br>Команда {appBaseName}</p>
                </div>
            </body>
            </html>
            """
            
            msg.attach(MIMEText(html_content, 'html'))
            
            # Явное преобразование типов
            host = str(mailHost)
            port = int(mailPort)
            username = str(mailUsername)
            password = str(mailPassword)
            
            if mailEncryption == "ssl":
                context = ssl.create_default_context()
                with smtplib.SMTP_SSL(host, port, context=context) as server:
                    server.login(username, password)
                    server.send_message(msg)
            else:
                with smtplib.SMTP(host, port) as server:
                    if mailEncryption == "tls":
                        server.starttls()
                    server.login(username, password)
                    server.send_message(msg)
                
            return True
            
        except Exception as e:
            logger.error(f"Ошибка отправки welcome email: {e}", exc_info=True)
            return False