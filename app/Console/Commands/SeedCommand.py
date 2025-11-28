# app/Console/Commands/SeedCommand.py
from database.seeders.database_seeder import seed
from app.Console.Commands.Command import Command

class SeedCommand(Command):
    @property
    def signature(self) -> str:
        return "db:seed"

    @property
    def description(self) -> str:
        return "Наполнить базу начальными данными"

    def handle(self, args=None) -> int:
        seed()
        return 0


