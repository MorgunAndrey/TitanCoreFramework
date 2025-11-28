# app/Console/Commands/MakeMigrationCommand.py
from typing import List, Optional
from datetime import datetime
from pathlib import Path
from app.Console.Commands.Command import Command
import re

class MakeMigrationCommand(Command):
    @property
    def signature(self) -> str:
        return "make:migration {name}"
    
    @property
    def description(self) -> str:
        return "Создать новую миграцию базы данных"
    
    def handle(self, args: Optional[List[str]] = None) -> int:
        if not args or len(args) < 1:
            self.print_error("Укажите имя миграции")
            return 1

        table_name = args[0]
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{timestamp}_create_{table_name}_table.py"
        migrations_dir = Path("database/migrations/versions")
        migrations_dir.mkdir(exist_ok=True)

        revision = timestamp
        down_revision = self._get_last_revision(migrations_dir)

        template = self._generate_migration(table_name, revision, down_revision)

        with open(migrations_dir / filename, "w") as f:
            f.write(template)
        
        self.print_info(f"Создана миграция: {filename}")
        return 0
    
    def _get_last_revision(self, path: Path) -> Optional[str]:
        migration_files = sorted(path.glob("*.py"))
        if not migration_files:
            return None

        last_file = migration_files[-1]
        content = last_file.read_text(encoding="utf-8")
        match = re.search(r"revision\s*=\s*['\"](.+?)['\"]", content)
        if match:
            return match.group(1)
        return None
    
    def _generate_migration(self, table_name: str, revision: str, down_revision: Optional[str]) -> str:
        down_rev_str = f"'{down_revision}'" if down_revision else "None"
        return f'''\"\"\"
Create {table_name} table
\"\"\"

from alembic import op
import sqlalchemy as sa

revision = '{revision}'
down_revision = {down_rev_str}
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        '{table_name}',
        sa.Column('id', sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.func.now(), onupdate=sa.func.now())
    )

def downgrade():
    op.drop_table('{table_name}')
'''