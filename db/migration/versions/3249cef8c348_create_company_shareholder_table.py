"""create company shareholder table

Revision ID: 3249cef8c348
Revises: 03f6be3826c5
Create Date: 2021-04-19 05:45:21.752605

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import func


# revision identifiers, used by Alembic.
revision = '3249cef8c348'
down_revision = '03f6be3826c5'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
		'company_shareholder',
		sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
		sa.Column('shareholder_id', sa.Integer, sa.ForeignKey('shareholder.id')),
		sa.Column('company_id', sa.Integer, sa.ForeignKey('company.id')),
		sa.Column('share', sa.BigInteger, nullable=False),
		sa.Column('create_date', sa.DateTime(timezone=False), default=func.now(), nullable=False),
		sa.Column('update_date', sa.DateTime(timezone=False), default=func.now(), nullable=False),
	)


def downgrade():
    op.drop_table('company_shareholder')
