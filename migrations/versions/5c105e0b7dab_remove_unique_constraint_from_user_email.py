"""Remove unique constraint from User.email

Revision ID: 5c105e0b7dab
Revises: 
Create Date: 2018-05-28 21:15:37.706486

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5c105e0b7dab'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('book',
    sa.Column('id', sa.String(length=15), nullable=False),
    sa.Column('book_name', sa.String(length=200), nullable=True),
    sa.Column('genre', sa.String(length=200), nullable=False),
    sa.Column('author', sa.String(length=300), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=30), nullable=False),
    sa.Column('first_name', sa.String(length=20), nullable=True),
    sa.Column('last_name', sa.String(length=20), nullable=True),
    sa.Column('email', sa.String(length=80), nullable=False),
    sa.Column('preferences', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('username')
    )
    op.create_table('user_book',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('book_id', sa.String(length=15), nullable=False),
    sa.Column('finished', sa.Boolean(), nullable=True),
    sa.Column('added_date', sa.DateTime(), nullable=True),
    sa.Column('notes', sa.String(length=1000), nullable=True),
    sa.Column('topics', sa.String(length=1000), nullable=True),
    sa.ForeignKeyConstraint(['book_id'], ['book.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('user_id', 'book_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_book')
    op.drop_table('user')
    op.drop_table('book')
    # ### end Alembic commands ###