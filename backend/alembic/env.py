import os
from logging.config import fileConfig
from sqlalchemy import create_engine, pool
from alembic import context

config = context.config
fileConfig(config.config_file_name)

from app.models.user import User
from app.models.otp import OTP
from app.models.food import FoodItem
from app.models.cart import CartItem
from app.models.order import Order, OrderItem
from app.database import Base

target_metadata = Base.metadata

def get_url():
    return os.environ.get("DB_URL") or config.get_main_option("sqlalchemy.url")

def run_migrations_offline():
    context.configure(url=get_url(), target_metadata=target_metadata, literal_binds=True)
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    connectable = create_engine(get_url(), poolclass=pool.NullPool)
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
