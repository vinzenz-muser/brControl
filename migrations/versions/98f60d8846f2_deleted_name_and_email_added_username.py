"""deleted name and email, added username

Revision ID: 98f60d8846f2
Revises: 4ea1d96d21ae
Create Date: 2020-12-30 18:59:27.275263

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '98f60d8846f2'
down_revision = '4ea1d96d21ae'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('username', sa.String(length=64), nullable=False, unique=True))
    op.create_unique_constraint(None, 'user', ['username'])
    op.drop_column('user', 'name')
    op.drop_column('user', 'email')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('email', mysql.VARCHAR(length=64), nullable=False))
    op.add_column('user', sa.Column('name', mysql.VARCHAR(length=64), nullable=False))
    op.drop_constraint(None, 'user', type_='unique')
    op.drop_column('user', 'username')
    # ### end Alembic commands ###
