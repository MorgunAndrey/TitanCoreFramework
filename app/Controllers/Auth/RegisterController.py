# app/Controllers/Auth/RegisterController.py      
from fastapi import Request, Depends, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from config.templates import templates
from app.Models.User import User
from sqlalchemy.orm import Session
from config.database import get_db
from app.Services.RequestParser import RequestParser
from email_validator import validate_email, EmailNotValidError
from app.Services.CsrfService import CsrfService
from app.Services.EmailService import EmailService
import re
import logging
from datetime import datetime
from app.Services.AuthService import AuthService

logger = logging.getLogger(__name__)

class RegisterController():
    
    @staticmethod
    async def register(request: Request) -> HTMLResponse:
     
        csrf_token = CsrfService.set_token_to_session(request)
        return templates.TemplateResponse("auth/auth.html", {
            "request": request,
            "csrf_token": csrf_token
        }) 

    @staticmethod
    async def siteRegister(request: Request, db: Session = Depends(get_db)):
        try:
            request_data = await RequestParser.parse_request(request)

            token = request_data.get("token")
            csrf_token = request_data.get("csrf_token")
            name = request_data.get("name")
            email = request_data.get("email")
            password = request_data.get("password")

            if not CsrfService.validate_token(request, csrf_token):
                return JSONResponse(
                    {"error": "Некорректный CSRF-токен", "csrf": CsrfService.set_token_to_session(request)},
                    status_code=400
                )

            if not name:
                return JSONResponse(
                    {"error": "Пожалуйста, введите имя", "csrf": CsrfService.set_token_to_session(request)},
                    status_code=400
                )

            # Валидация имени на сервере
            name = name.strip()
            if len(name) < 2 or len(name) > 255:
                return JSONResponse(
                    {"error": "Имя должно содержать от 2 до 255 символов", "csrf": CsrfService.set_token_to_session(request)},
                    status_code=400
                )
            
            name_pattern = re.compile(r"^[a-zA-Zа-яА-ЯёЁ\s\-]+$")
            if not name_pattern.match(name):
                return JSONResponse(
                    {"error": "Имя содержит недопустимые символы", "csrf": CsrfService.set_token_to_session(request)},
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
            
            # Валидация пароля ПЕРЕД проверкой существования пользователя (защита от timing attack)
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
            
            # Проверка существования пользователя после валидации
            user = db.query(User).filter_by(
                email=email
            ).first()
            
            if user:
                return JSONResponse(
                    {"error": "Ошибка пользователя с указанным E-mail.", "csrf": CsrfService.set_token_to_session(request)},
                    status_code=409
                )

            password_hash = AuthService.get_password_hash(password)
            
            # Использование транзакции для согласованности данных
            try:
                new_user = User(
                    name=name,
                    email=email,
                    password=password_hash,
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow()
                )
                
                db.add(new_user)
                db.flush()  # Получаем ID без commit
                
                from app.Models.UsersPasswordHistory import UsersPasswordHistory
                password_history = UsersPasswordHistory(
                    user_id=new_user.id,
                    password=password_hash,
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow()
                )
                db.add(password_history)
                db.commit()  # Один commit для обеих операций
                
                return JSONResponse(
                    {"result": 1, "csrf": CsrfService.set_token_to_session(request)},
                    status_code=200
                )
            except Exception as e:
                db.rollback()
                raise

                        
        except Exception as e:
            # Логируем детали ошибки на сервере, но не раскрываем клиенту
            logger.error(f"Registration error: {str(e)}", exc_info=True)
            return JSONResponse(
                {"error": "Произошла ошибка при обработке запроса", "csrf": CsrfService.generate_token()},
                status_code=500
            )          