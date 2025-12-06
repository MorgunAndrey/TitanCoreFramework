# app/Middleware/not_auth.py
from fastapi import Request,HTTPException

async def not_auth_redirect(request: Request):
    if not request.session.get("user_id"):  # Если не авторизован
        raise HTTPException(status_code=302, headers={"Location": "/"})
        
