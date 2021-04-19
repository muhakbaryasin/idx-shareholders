"""create shareholder table

Revision ID: 03f6be3826c5
Revises: 8262700bb560
Create Date: 2021-04-19 05:30:41.458333

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import func


# revision identifiers, used by Alembic.
revision = '03f6be3826c5'
down_revision = '8262700bb560'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
		'shareholder',
		sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
		sa.Column('name', sa.String(255), index=True, unique=True, nullable=False),
		sa.Column('share', sa.BigInteger, nullable=False),
		sa.Column('create_date', sa.DateTime(timezone=False), default=func.now(), nullable=False),
		sa.Column('update_date', sa.DateTime(timezone=False), default=func.now(), nullable=False),
	)


def downgrade():
    op.drop_table('shareholder')
