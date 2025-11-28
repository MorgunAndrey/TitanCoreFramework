import secrets
from fastapi import Request
from typing import Optional

class CsrfService:
    CSRF_TOKEN_LENGTH = 32
    CSRF_TOKEN_NAME = "csrf_token"
    CSRF_HEADER_NAME = "X-CSRF-TOKEN"

    @staticmethod
    def generate_token() -> str:
        """Генерация нового CSRF токена"""
        return secrets.token_hex(CsrfService.CSRF_TOKEN_LENGTH)

    @staticmethod
    def get_token_from_session(request: Request) -> Optional[str]:
        """Получение CSRF токена из сессии"""
        return request.session.get(CsrfService.CSRF_TOKEN_NAME)

    @staticmethod
    def validate_token(request: Request, token: str) -> bool:
        """Валидация CSRF токена"""
        session_token = CsrfService.get_token_from_session(request)
        return session_token is not None and secrets.compare_digest(session_token, token)

    @staticmethod
    def set_token_to_session(request: Request, token: Optional[str] = None) -> str:
        """Установка CSRF токена в сессию"""
        if token is None:
            token = CsrfService.generate_token()
        request.session[CsrfService.CSRF_TOKEN_NAME] = token
        return token