    
# app/Controllers/Auth/LoginController.py

from fastapi import Request, Depends
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from config.templates import templates
from app.Models.User import User
from sqlalchemy.orm import Session
from config.database import get_db
from typing import AsyncGenerator
from app.Services.RequestParser import RequestParser
from email_validator import validate_email, EmailNotValidError
import re
import logging
from app.Services.CsrfService import CsrfService
from app.Services.AuthService import AuthService
from app.Services.RateLimitService import RateLimitService

logger = logging.getLogger(__name__)

class LoginController:
    
    @staticmethod
    async def login(request: Request) -> HTMLResponse:
     
        csrf_token = CsrfService.set_token_to_session(request)
        return templates.TemplateResponse("auth/auth.html", {
            "request": request,
            "csrf_token": csrf_token
        })
    

    @staticmethod
    async def authLogin(request: Request, db: Session = Depends(get_db)):
        try:
            
            
            request_data = await RequestParser.parse_request(request)
            csrf_token = request_data.get("csrf_token")
            email = request_data.get("login")
            password = request_data.get("password")

            client_ip = request.client.host if request.client else "unknown"
            rate_key = f"login:{client_ip}"
            if not RateLimitService.check_and_increment(rate_key, limit=5, window_seconds=300):
                return JSONResponse(
                    {"error": "Слишком много попыток, попробуйте позже", "csrf": CsrfService.set_token_to_session(request)},
                    status_code=429
                )

            if not CsrfService.validate_token(request, csrf_token):
                return JSONResponse(
                    {"error": "Некорректный CSRF-токен", "csrf": CsrfService.set_token_to_session(request)},
                    status_code=400
                )            

            if not email:
                return JSONResponse(
                    {"error": "Пожалуйста, введите email", "csrf": CsrfService.set_token_to_session(request)},
                    status_code=400
                )
            
            if not password:
                return JSONResponse(
                    {"error": "Пожалуйста, введите пароль", "csrf": CsrfService.set_token_to_session(request)},
                    status_code=400
                )

            try:
                valid = validate_email(email)
                email = valid.email 
            except EmailNotValidError as e:
                return JSONResponse(
                    {"error": "Пожалуйста, введите корректный email", "csrf": CsrfService.set_token_to_session(request)},
                    status_code=400
                )
            
            password_pattern = re.compile(r"(?=^.{10,72}$)(?=.*[A-Z])(?=.*[0-9])(?=.*[a-z])(?=.*[^\w\s]).*")
            if not password_pattern.fullmatch(password):
                return JSONResponse(
                    {
                        "error": "Пароль должен содержать:\n"
                        "- Не менее 10 символов\n"
                        "- Минимум 1 заглавную букву\n"
                        "- Минимум 1 цифру\n"
                        "- Минимум 1 спецсимвол",
                        "csrf": CsrfService.set_token_to_session(request)
                    },
                    status_code=400
                )

            # Удалено лишнее хеширование пароля - проверка происходит через verify_password
            
            user = db.query(User).filter_by(
                email=email,
            ).first()

            user_verify = user and AuthService.verify_password(password, user.password)
            
            if not user_verify:
                # Единое сообщение, чтобы не раскрывать наличие пользователя
                return JSONResponse(
                    {"error": "Неверные учетные данные", "csrf": CsrfService.set_token_to_session(request)},
                    status_code=401
                )
            
            request.session["user_id"] = user.id
            request.session["user_name"] = user.name
            request.session["user_email"] = user.email

            # Генерируем новый токен после успешной аутентификации
            new_csrf_token = CsrfService.set_token_to_session(request)
            
            return JSONResponse(
                {"result": 1, "url": "/main", "csrf": new_csrf_token}
            )
            
        except Exception as e:
            # Логируем детали ошибки на сервере, но не раскрываем клиенту
            logger.error(f"Login error: {str(e)}", exc_info=True)
            return JSONResponse(
                {"error": "Произошла ошибка при обработке запроса", "csrf": CsrfService.generate_token()},
                status_code=500
            )

    @staticmethod
    async def logout(request: Request) -> RedirectResponse:
        request.session.clear()
        return RedirectResponse(url="/")