# app/Console/Commands/MakeModelCommand.py
import os
from pathlib import Path
from typing import List, Optional
from app.Console.Commands.Command import Command

class MakeModelCommand(Command):
    @property
    def signature(self) -> str:
        return "make:model {name}"
    
    @property
    def description(self) -> str:
        return "Создать новую модель SQLAlchemy"
    
    def handle(self, args: Optional[List[str]] = None) -> int:
        if not args or len(args) == 0:
            self.print_error("Укажите имя модели")
            return 1
        
        name = args[0]
        
        try:
            content = self._generate_model_template(name)
            
            path = Path(f"app/Models/{name}.py")
            path.parent.mkdir(exist_ok=True, parents=True)
            
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
            
            self.print_info(f"Модель {name} создана: {path}")
            return 0
        except Exception as e:
            self.print_error(f"Ошибка: {str(e)}")
            return 1
    
    def _generate_model_template(self, model_name: str) -> str:
        # Автоматически преобразуем имя модели в snake_case для имени таблицы
        table_name = self._camel_to_snake(model_name)
        
        return f'''from sqlalchemy import Column, BigInteger, String, DateTime
from datetime import datetime
from config.database import Base

class {model_name}(Base):
    __tablename__ = "{table_name}"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<{model_name}>"
'''
    
    def _camel_to_snake(self, name: str) -> str:
        """Преобразует CamelCase в snake_case"""
        import re
        # Вставляем подчеркивание перед заглавными буквами и переводим в нижний регистр
        snake = re.sub('([A-Z])', r'_\1', name).lower()
        # Убираем ведущее подчеркивание если оно есть
        if snake.startswith('_'):
            snake = snake[1:]
        return snake