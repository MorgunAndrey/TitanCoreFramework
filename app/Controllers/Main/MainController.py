# app/Controllers/Main/MainController.py

from fastapi import Request
from fastapi.responses import HTMLResponse
from config.templates import templates

class MainController:
    @staticmethod
    async def main(request: Request) -> HTMLResponse:
        user_name = request.session.get("user_name","Гость")
        return templates.TemplateResponse(
            "main/index.html", 
            {
                "request": request,
                "user_name": user_name
            }
        )
    
   

  

