"""Agregando campo created en Comment

Revision ID: a1dcb5ef331b
Revises: 9d2fb7e29d36
Create Date: 2022-01-23 00:14:53.679498

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'a1dcb5ef331b'
down_revision = '9d2fb7e29d36'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('comment', sa.Column('created', sa.DateTime(), nullable=True))
    op.drop_column('comment', 'create')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('comment', sa.Column('create', postgresql.TIMESTAMP(), autoincrement=False, nullable=True))
    op.drop_column('comment', 'created')
    # ### end Alembic commands ###
