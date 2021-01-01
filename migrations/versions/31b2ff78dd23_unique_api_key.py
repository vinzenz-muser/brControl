"""Unique API-Key

Revision ID: 31b2ff78dd23
Revises: 5090363b0039
Create Date: 2020-12-31 13:11:18.488983

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '31b2ff78dd23'
down_revision = '5090363b0039'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'device', ['apiKey'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'device', type_='unique')
    # ### end Alembic commands ###