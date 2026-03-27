"""initial schema

Revision ID: 0001
Revises: 
Create Date: 2026-03-27

"""
from alembic import op
import sqlalchemy as sa

revision = '0001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), primary_key=True, index=True),
        sa.Column('name', sa.String(100), nullable=False),
        sa.Column('email', sa.String(150), unique=True, index=True, nullable=False),
        sa.Column('hashed_password', sa.String(255), nullable=False),
        sa.Column('is_verified', sa.Boolean(), default=False),
    )
    op.create_table(
        'otps',
        sa.Column('id', sa.Integer(), primary_key=True, index=True),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('code', sa.String(6), nullable=False),
        sa.Column('expires_at', sa.DateTime(), nullable=False),
        sa.Column('used', sa.Boolean(), default=False),
        sa.Column('created_at', sa.DateTime()),
    )
    op.create_table(
        'food_items',
        sa.Column('id', sa.Integer(), primary_key=True, index=True),
        sa.Column('name', sa.String(150), nullable=False),
        sa.Column('description', sa.Text()),
        sa.Column('price', sa.Float(), nullable=False),
        sa.Column('image_url', sa.String(500)),
        sa.Column('category', sa.String(100), default='Main'),
        sa.Column('available', sa.Boolean(), default=True),
    )
    op.create_table(
        'cart_items',
        sa.Column('id', sa.Integer(), primary_key=True, index=True),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('food_item_id', sa.Integer(), sa.ForeignKey('food_items.id'), nullable=False),
        sa.Column('quantity', sa.Integer(), default=1),
    )
    op.create_table(
        'orders',
        sa.Column('id', sa.Integer(), primary_key=True, index=True),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('total_price', sa.Float(), nullable=False),
        sa.Column('status', sa.String(50), default='pending'),
        sa.Column('created_at', sa.DateTime()),
    )
    op.create_table(
        'order_items',
        sa.Column('id', sa.Integer(), primary_key=True, index=True),
        sa.Column('order_id', sa.Integer(), sa.ForeignKey('orders.id'), nullable=False),
        sa.Column('food_item_id', sa.Integer(), sa.ForeignKey('food_items.id'), nullable=False),
        sa.Column('quantity', sa.Integer(), nullable=False),
        sa.Column('unit_price', sa.Float(), nullable=False),
    )


def downgrade() -> None:
    op.drop_table('order_items')
    op.drop_table('orders')
    op.drop_table('cart_items')
    op.drop_table('food_items')
    op.drop_table('otps')
    op.drop_table('users')
