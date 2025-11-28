"""
Create users_password_history table
"""

from alembic import op
import sqlalchemy as sa

revision = '20250823_135521'
down_revision = '20250725_003757'
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        'users_password_history',
        sa.Column('id', sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column('user_id', sa.BigInteger(), nullable=False),
        sa.Column('password', sa.String(length=255), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.func.now(), onupdate=sa.func.now())
    )

def downgrade():
    op.drop_table('users_password_history')
