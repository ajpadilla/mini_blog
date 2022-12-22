"""empty message

Revision ID: ed44096d6e3d
Revises: 2f590722713a
Create Date: 2022-08-27 21:37:42.622983

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ed44096d6e3d'
down_revision = '2f590722713a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user_cart',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('shopping_cart_id', sa.Integer(), nullable=False),
    sa.Column('status', sa.String(length=30), nullable=False),
    sa.Column('payment_date', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['shopping_cart_id'], ['shopping_cart.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['blog_user.id'], ),
    sa.PrimaryKeyConstraint('id', 'user_id', 'shopping_cart_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_cart')
    # ### end Alembic commands ###