# app/Middleware/auth.py
from fastapi import Request, HTTPException

async def auth_redirect(request: Request):
    if request.session.get("user_id"):
        # Пользователь авторизован → редиректим на /main
        raise HTTPException(status_code=302, headers={"Location": "/main"})
