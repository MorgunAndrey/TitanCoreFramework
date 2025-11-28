"""
database/migration/versions/20250725_001554_create_users_table.py
Migration for creating 'users' table.
"""

from alembic import op
import sqlalchemy as sa

# Alembic identifiers (ОБЯЗАТЕЛЬНО)
revision = '20250725_001554'  # Уникальный ID миграции
down_revision = None           # ID предыдущей миграции или None, если это первая
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False, unique=True),
        sa.Column('email_verified_at', sa.DateTime(), nullable=True),
        sa.Column('password', sa.String(length=255), nullable=False),
        sa.Column('remember_token', sa.String(length=100), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), nullable=False, 
                  server_default=sa.func.now(), onupdate=sa.func.now())
    )

def downgrade():
    op.drop_table('users')
