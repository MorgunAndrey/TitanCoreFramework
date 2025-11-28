from alembic import op
import sqlalchemy as sa

# Alembic identifiers (ОБЯЗАТЕЛЬНО)
revision = '20250725_003757'
down_revision = '20250725_001554' 
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        'users_password_reset_tokens',
        sa.Column('id', sa.BigInteger(), autoincrement=True,primary_key=True, nullable=False),
        sa.Column('email', sa.String(length=255), primary_key=True),
        sa.Column('token', sa.String(length=255), nullable=False, unique=True),
        sa.Column('created_at', sa.DateTime(), nullable=True, server_default=sa.func.now())
    )

def downgrade():
    op.drop_table('users_password_reset_tokens')
