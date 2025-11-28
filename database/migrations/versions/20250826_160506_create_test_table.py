"""
Create test table
"""

from alembic import op
import sqlalchemy as sa

revision = '20250826_160506'
down_revision = '20250823_135521'
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        'test',
        sa.Column('id', sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.func.now(), onupdate=sa.func.now())
    )

def downgrade():
    op.drop_table('test')
