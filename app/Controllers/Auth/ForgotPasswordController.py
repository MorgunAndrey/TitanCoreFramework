    
from fastapi import Request, Depends, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from config.templates import templates
from app.Services.CsrfService import CsrfService
from sqlalchemy.orm import Session
from config.database import get_db
from app.Models.User import User
from app.Services.RequestParser import RequestParser
from app.Models.UsersPasswordResetToken import UsersPasswordResetToken
from email_validator import validate_email, EmailNotValidError
from app.Services.EmailService import EmailService
import hashlib
import logging
from app.Services.RateLimitService import RateLimitService

logger = logging.getLogger(__name__)

class ForgotPasswordController():
    @staticmethod
    async def forgotPassword(request: Request) -> HTMLResponse:
        csrf_token = CsrfService.set_token_to_session(request)
        return templates.TemplateResponse("auth/auth.html", {
            "request": request,
            "csrf_token": csrf_token
        })
    @staticmethod
    async def passwordEmail(request: Request, db: Session = Depends(get_db)):
        try:
            request_data = await RequestParser.parse_request(request)
            csrf_token = request_data.get("csrf_token")
            email = request_data.get("email")

            client_ip = request.client.host if request.client else "unknown"
            rate_key = f"password_email:{client_ip}"
            if not RateLimitService.check_and_increment(rate_key, limit=5, window_seconds=900):
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
            

            try:
                valid = validate_email(email)
                email = valid.email 
            except EmailNotValidError as e:
                return JSONResponse(
                    {"error": "Пожалуйста, введите корректный email", "csrf": CsrfService.set_token_to_session(request)},
                    status_code=400
                )
            user = db.query(User).filter_by(
                email=email
            ).first()
            
            # Защита от перечисления пользователей - всегда возвращаем одинаковый ответ
            # Отправляем email только если пользователь существует
            if user:
                mail_token = CsrfService.generate_token()
                mail_token_hash = hashlib.sha256(mail_token.encode()).hexdigest()
                email_sent = EmailService.send_password_reset_email(email, mail_token)
                
                # Если email успешно отправлен, сохраняем токен в БД
                if email_sent:
                    try:
                        db.query(UsersPasswordResetToken).filter(
                            UsersPasswordResetToken.email == email
                        ).delete()
                        
                        reset_token = UsersPasswordResetToken(
                            email=email,
                            token=mail_token_hash
                        )
                        
                        db.add(reset_token)
                        db.commit()
                    except Exception as e:
                        db.rollback()
                        logger.error(f"Failed to save password reset token for {email}: {e}", exc_info=True)
                        # Логируем ошибку, но все равно возвращаем успех для защиты от перечисления
                else:
                    # Email не отправлен - логируем критическую ошибку для администратора
                    logger.error(f"CRITICAL: Failed to send password reset email to {email}. Token was NOT saved.", exc_info=True)
                    # Не сохраняем токен, так как email не был отправлен
                    # Все равно возвращаем успех для защиты от перечисления пользователей
            
            # Всегда возвращаем одинаковый ответ для защиты от перечисления пользователей
            # (даже если email не был отправлен - это логируется для администратора)
            return JSONResponse(
                {"result": 1},
                status_code=200
            )
                       
        except Exception as e:
            # Логируем детали ошибки на сервере, но не раскрываем клиенту
            logger.error(f"Forgot password error: {str(e)}", exc_info=True)
            return JSONResponse(
                {"error": "Произошла ошибка при обработке запроса", "csrf": CsrfService.generate_token()},
                status_code=500
            )          