"""add category and fix image_url to food_items

Revision ID: 0002
Revises: 0001
Create Date: 2026-03-27

"""
from alembic import op
import sqlalchemy as sa

revision = '0002'
down_revision = '0001'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('food_items', sa.Column('category', sa.String(100), nullable=True, server_default='Main'))
    op.alter_column('food_items', 'image_url', type_=sa.String(500), existing_nullable=True)


def downgrade() -> None:
    op.drop_column('food_items', 'category')
    op.alter_column('food_items', 'image_url', type_=sa.String(300), existing_nullable=True)
