    
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
            
            if not user:
                return JSONResponse(
                    {"error": "Не удалось найти пользователя с указанным E-mail.", "csrf": CsrfService.set_token_to_session(request)},
                    status_code=401
                )
            if user:
                mail_token = CsrfService.generate_token()
                mail_token_hash = hashlib.sha256(mail_token.encode()).hexdigest()
                email_sent = EmailService.send_password_reset_email(email, mail_token)
                
                db.query(UsersPasswordResetToken).filter(
                    UsersPasswordResetToken.email == email
                ).delete()
                
                reset_token = UsersPasswordResetToken(
                    email=email,
                    token=mail_token_hash
                )
                
                db.add(reset_token)
                db.commit()
            
                if email_sent:
                    return JSONResponse(
                        {"result": 1},
                        status_code=200
            )    
                       
        except Exception as e:
            return JSONResponse(
                {"error": f"Ошибка сервера: {str(e)}", "csrf": CsrfService.generate_token()},
                status_code=500
            )          