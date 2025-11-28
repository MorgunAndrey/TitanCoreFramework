#app/Console/Commands/MakeControllerCommand.py
import os
from pathlib import Path
from typing import List, Optional
from jinja2 import Template
from app.Console.Commands.Command import Command

class MakeControllerCommand(Command):
    @property
    def signature(self) -> str:
        return "make:controller {name} {--api}"
    
    @property
    def description(self) -> str:
        return "Создать новый контроллер"
    
    def handle(self, args: Optional[List[str]] = None) -> int:
        if not args or len(args) == 0:
            self.print_error("Укажите имя контроллера")
            return 1
        
        name = args[0]
        is_api = "--api" in args
        
        try:
            template = self._get_template(is_api)
            content = template.render(controller_name=name)
            
            path = self._get_controller_path(name, is_api)
            path.parent.mkdir(exist_ok=True, parents=True)
            
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
            
            self.print_info(f"Контроллер {name} создан: {path}")
            return 0
        except Exception as e:
            self.print_error(f"Ошибка: {str(e)}")
            return 1
    
    def _get_template(self, is_api: bool) -> Template:
        template_str = '''    
from fastapi import Request
from fastapi.responses import HTMLResponse
from config.templates import templates

class {{ controller_name }}Controller():
    @staticmethod
    async def index(request: Request) -> HTMLResponse:
        return templates.TemplateResponse("{{ controller_name|lower }}.html", {"request": request})            
'''
        return Template(template_str)
    
    def _get_controller_path(self, name: str, is_api: bool) -> Path:
        folder = "Controllers" if not is_api else "Controllers/API"
        return Path(f"app/{folder}/{name}Controller.py")