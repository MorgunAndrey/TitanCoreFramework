# app/Controllers/Auth/ResetPasswordController.py   
from fastapi import Request, Depends, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from config.templates import templates
from app.Models.User import User
from app.Models.UsersPasswordResetToken import UsersPasswordResetToken
from app.Models.UsersPasswordHistory import UsersPasswordHistory
from sqlalchemy.orm import Session
from config.database import get_db
from app.Services.RequestParser import RequestParser
from email_validator import validate_email, EmailNotValidError
from app.Services.CsrfService import CsrfService
from app.Services.EmailService import EmailService
from app.Services.AuthService import AuthService
from app.Services.RateLimitService import RateLimitService
import hashlib
import re
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class ResetPasswordController():
    
    @classmethod
    async def resetPassword(cls, request: Request, token: str, db: Session = Depends(get_db)):
        try:
            if not token:
                raise HTTPException(status_code=302, headers={"Location": "/"})

            token_hash = hashlib.sha256(token.encode()).hexdigest()
            reset_token = db.query(UsersPasswordResetToken).filter(
                UsersPasswordResetToken.token == token_hash
            ).first()

            if not reset_token:
                raise HTTPException(status_code=302, headers={"Location": "/"})
                    
            if reset_token.is_expired():
                raise HTTPException(status_code=302, headers={"Location": "/"})

            csrf_token = CsrfService.set_token_to_session(request)
            return templates.TemplateResponse("auth/auth.html", {
                "request": request,
                "csrf_token": csrf_token
            })
        except Exception as e:
            raise HTTPException(status_code=302, headers={"Location": "/"})
    
    @staticmethod
    async def passwordСhange(request: Request, db: Session = Depends(get_db)):
        try:
            request_data = await RequestParser.parse_request(request)
            token = request_data.get("token")
            csrf_token = request_data.get("csrf_token")
            email = request_data.get("email")
            password = request_data.get("password")

            client_ip = request.client.host if request.client else "unknown"
            rate_key = f"password_change:{client_ip}"
            if not RateLimitService.check_and_increment(rate_key, limit=5, window_seconds=900):
                return JSONResponse(
                    {"error": "Слишком много попыток, попробуйте позже", "csrf": CsrfService.set_token_to_session(request)},
                    status_code=429
                )
            
            if not token:
                return JSONResponse(
                    {"error": "Отсутствует токен сброса", "csrf": CsrfService.set_token_to_session(request)},
                    status_code=400
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
            
            token_hash = hashlib.sha256(token.encode()).hexdigest()
            reset_token = db.query(UsersPasswordResetToken).filter(
                UsersPasswordResetToken.token == token_hash
            ).first()
            
            if not reset_token or reset_token.email != email:
                return JSONResponse(
                    {"error": "Некорректный или устаревший токен сброса", "csrf": CsrfService.set_token_to_session(request)},
                    status_code=401
                )
            
            if reset_token.is_expired():
                db.query(UsersPasswordResetToken).filter(
                    UsersPasswordResetToken.token == token_hash
                ).delete()
                db.commit()
                return JSONResponse(
                    {"error": "Срок действия токена истек", "csrf": CsrfService.set_token_to_session(request)},
                    status_code=400
                )
            
            user = db.query(User).filter_by(
                email=email
            ).first()
            
            # Защита от перечисления пользователей - используем общее сообщение
            if not user:
                return JSONResponse(
                    {"error": "Некорректный или устаревший токен сброса", "csrf": CsrfService.set_token_to_session(request)},
                    status_code=401
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
            
            password_hash = AuthService.get_password_hash(password)
            
            # Проверяем, использовался ли пароль ранее
            password_reused = False
            password_history_entries = db.query(UsersPasswordHistory).filter(
                UsersPasswordHistory.user_id == user.id
            ).all()

            if AuthService.verify_password(password, user.password):
                password_reused = True
            else:
                for history_record in password_history_entries:
                    if AuthService.verify_password(password, history_record.password):
                        password_reused = True
                        break

            if password_reused:
                return JSONResponse(
                    {"error": "Нельзя использовать старый пароль. Придумайте новый пароль.", "csrf": CsrfService.set_token_to_session(request)},
                    status_code=400
                )
            
            # Использование транзакции для согласованности данных
            try:
                db.query(UsersPasswordResetToken).filter(
                    UsersPasswordResetToken.email == email
                ).delete()

                db.query(User).filter(
                    User.email == email
                ).update(
                    {"password": password_hash}
                )
                
                password_history = UsersPasswordHistory(
                    user_id=user.id,
                    password=password_hash,
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow()
                )
                db.add(password_history)
                
                db.commit()
                
                return JSONResponse(
                    {"result": 1},
                    status_code=200
                )
            except Exception as e:
                db.rollback()
                raise  

                        
        except Exception as e:
            # Логируем детали ошибки на сервере, но не раскрываем клиенту
            logger.error(f"Password reset error: {str(e)}", exc_info=True)
            return JSONResponse(
                {"error": "Произошла ошибка при обработке запроса", "csrf": CsrfService.generate_token()},
                status_code=500
            )

    