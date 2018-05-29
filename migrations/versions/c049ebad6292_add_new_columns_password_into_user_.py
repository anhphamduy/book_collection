"""Add new columns password into User. Previously, without column password, when invoking set_password method in User class, nothing happens as column password is missing. This upgrade will help fixing this bug

Revision ID: c049ebad6292
Revises: 5c105e0b7dab
Create Date: 2018-05-28 21:23:06.200344

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c049ebad6292'
down_revision = '5c105e0b7dab'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('password', sa.String(length=128), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'password')
    # ### end Alembic commands ###