#app/Console/MigrateCommand.py
from typing import List, Optional
from alembic.config import Config
from alembic import command
from app.Console.Commands.Command import Command
from pathlib import Path
import os

class MigrateCommand(Command):
    @property
    def signature(self) -> str:
        return "migrate {--fresh} {--init}"
    
    @property
    def description(self) -> str:
        return "Управление миграциями базы данных"
    
    def handle(self, args: Optional[List[str]] = None) -> int:
        if args is None:
            args = []
            
        try:
            # Получаем корневую директорию проекта
            project_root = Path(__file__).resolve().parent.parent.parent.parent
            alembic_ini_path = project_root / "alembic.ini"
            migrations_dir = project_root / "database" / "migrations"
            
            # Проверяем наличие файла конфигурации
            if not alembic_ini_path.exists():
                self.print_error(f"Файл конфигурации не найден: {alembic_ini_path}")
                self.print_info("Создайте файл alembic.ini в корне проекта")
                return 1
            
            # Настройка Alembic
            alembic_cfg = Config(str(alembic_ini_path))
            alembic_cfg.set_main_option("script_location", str(migrations_dir))
            
            # Инициализация миграций (если нужно)
            if "--init" in args:
                if migrations_dir.exists():
                    self.print_error("Директория миграций уже существует!")
                    return 1
                
                os.makedirs(migrations_dir, exist_ok=True)
                command.init(alembic_cfg, str(migrations_dir))  # Исправлено здесь
                self.print_info(f"Инициализирована директория миграций: {migrations_dir}")
                return 0
            
            # Проверяем наличие директории миграций
            if not migrations_dir.exists():
                self.print_error(f"Директория миграций не найдена: {migrations_dir}")
                self.print_info("Используйте --init для инициализации")
                return 1
            
            # Выполнение миграций
            if "--fresh" in args:
                self.print_info("Выполняю сброс всех миграций...")
                command.downgrade(alembic_cfg, "base")
            
            self.print_info("Применяю миграции...")
            command.upgrade(alembic_cfg, "head")
            self.print_info("Миграции успешно применены")
            return 0
            
        except Exception as e:
            self.print_error(f"Ошибка при выполнении миграций: {str(e)}")
            return 1