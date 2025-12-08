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
import hashlib
import re
from datetime import datetime

class ResetPasswordController():
    
    @classmethod
    async def resetPassword(cls, request: Request, token: str, db: Session = Depends(get_db)):
        try:
            if not token:
                raise HTTPException(status_code=302, headers={"Location": "/"})

            reset_token = db.query(UsersPasswordResetToken).filter(
                UsersPasswordResetToken.token == token
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
            
            user = db.query(User).filter_by(
                email=email
            ).first()
            
            if not user:
                return JSONResponse(
                    {"error": "Не удалось найти пользователя с указанным E-mail.", "csrf": CsrfService.set_token_to_session(request)},
                    status_code=401
                )
            
            password_pattern = re.compile(r"((?=^.{7,}$)(?=.*[A-Z])(?=.*[0-9])(?=.*[a-z])[a-zA-Z0-9]*)")
            if not password_pattern.fullmatch(password):
                return JSONResponse(
                    {
                        "error": "Пароль должен содержать:\n"
                        "- Не менее 7 символов\n"
                        "- Минимум 1 заглавную букву\n"
                        "- Минимум 1 цифру\n"
                        "- Только латинские буквы и цифры",
                        "csrf": CsrfService.set_token_to_session(request)
                    },
                    status_code=400
                )
            
            password_hash = AuthService.get_password_hash(password)
            
            old_password = db.query(UsersPasswordHistory).filter(
                UsersPasswordHistory.user_id == user.id,
                UsersPasswordHistory.password == password_hash
            ).first()
            
            if old_password:
                return JSONResponse(
                    {"error": "Нельзя использовать старый пароль. Придумайте новый пароль.", "csrf": CsrfService.set_token_to_session(request)},
                    status_code=400
                )
            
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
            return JSONResponse(
                {"error": f"Ошибка сервера: {str(e)}", "csrf": CsrfService.generate_token()},
                status_code=500
            )

    