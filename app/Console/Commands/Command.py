#app/Console/Commands/Command.py
from abc import ABC, abstractmethod
from typing import List, Optional

class Command(ABC):
    @property
    @abstractmethod
    def signature(self) -> str:
        """Сигнатура команды (как вызывать)"""
        pass
    
    @property
    @abstractmethod
    def description(self) -> str:
        """Описание команды"""
        pass
    
    @abstractmethod
    def handle(self, args: Optional[List[str]] = None) -> int:
        """Логика выполнения команды"""
        pass
    
    def print_info(self, message: str):
        print(f"\033[94mINFO:\033[0m {message}")
    
    def print_error(self, message: str):
        print(f"\033[91mERROR:\033[0m {message}")