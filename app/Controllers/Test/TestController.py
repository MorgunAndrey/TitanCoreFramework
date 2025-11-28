# app/Controllers/Test/TestController.py
from fastapi import Request
from config.templates import templates

class TestController:
    @staticmethod
    async def index(request: Request):
        return templates.TemplateResponse("test/index.html", {"request": request})