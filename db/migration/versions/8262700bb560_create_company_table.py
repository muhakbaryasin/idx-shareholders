"""create company table

Revision ID: 8262700bb560
Revises: 
Create Date: 2021-04-19 04:34:47.867467

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import func


# revision identifiers, used by Alembic.
revision = '8262700bb560'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
	op.create_table(
		'company',
		sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
		sa.Column('name', sa.String(255), index=True, unique=True, nullable=False),
		sa.Column('code', sa.String(4), index=True, unique=True, nullable=False),
		sa.Column('listing_date', sa.DateTime(timezone=False), nullable=False),
		sa.Column('market_capitalization', sa.BigInteger, nullable=False),
		sa.Column('create_date', sa.DateTime(timezone=False), default=func.now(), nullable=False),
		sa.Column('update_date', sa.DateTime(timezone=False), default=func.now(), nullable=False),
	)


def downgrade():
	op.drop_table('company')
