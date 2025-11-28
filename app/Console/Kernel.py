# app/Console/Kernel.py
from typing import Dict, Type, List, Optional
from app.Console.Commands.Command import Command
from app.Console.Commands.MakeControllerCommand import MakeControllerCommand
from app.Console.Commands.MakeModelCommand import MakeModelCommand
from app.Console.Commands.MigrateCommand import MigrateCommand
from app.Console.Commands.MakeMigrationCommand import MakeMigrationCommand
from app.Console.Commands.SeedCommand import SeedCommand

class Kernel:
    def __init__(self):
        self.commands = self._register_commands()
    
    def _register_commands(self) -> Dict[str, Type[Command]]:
        return {
            'make:controller': MakeControllerCommand,
            'make:model': MakeModelCommand,
            'migrate': MigrateCommand,
            'make:migration': MakeMigrationCommand,
            'db:seed': SeedCommand,
        }
    
    def run(self, command: str, args: Optional[List[str]] = None) -> int:
        if command not in self.commands:
            print(f"Command {command} not found")
            return 1
        
        cmd = self.commands[command]()
        # Передаем все аргументы как есть
        return cmd.handle(args)