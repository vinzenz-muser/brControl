"""Removed ip

Revision ID: 47f865618dc0
Revises: f953cbfd2079
Create Date: 2021-01-16 21:06:26.559461

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '47f865618dc0'
down_revision = 'f953cbfd2079'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('hub_session', 'ip')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('hub_session', sa.Column('ip', mysql.VARCHAR(length=64), nullable=False))
    # ### end Alembic commands ###