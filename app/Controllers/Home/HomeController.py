# app/Controllers/Home/HomeController.py

from fastapi import Request
from fastapi.responses import HTMLResponse
from config.templates import templates

class HomeController:
    @staticmethod
    async def index(request: Request) -> HTMLResponse:
        user_name = request.session.get("user_name","Гость")

        return templates.TemplateResponse("home/index.html", {
                "request": request,
                "user_name": user_name
            })


