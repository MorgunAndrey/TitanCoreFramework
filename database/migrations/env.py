#app/database/migrations/env.py
from logging.config import fileConfig
from sqlalchemy import create_engine, pool
from alembic import context
import sys
from os.path import abspath, dirname
import warnings
import os
from app.Models.User import User  # и другие модели

sys.path.insert(0, dirname(dirname(dirname(abspath(__file__)))))


from config.database import DATABASE_URL, Base
from dotenv import load_dotenv

load_dotenv()


config = context.config


if config.config_file_name is not None:
    fileConfig(config.config_file_name)


target_metadata = Base.metadata

def run_migrations_offline() -> None:
    """Запуск миграций в offline-режиме."""
    url = config.get_main_option("sqlalchemy.url", DATABASE_URL)
    
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
        compare_server_default=True,
        render_as_batch=True,
        transaction_per_migration=True,
        user_module_prefix='sa.',
        include_schemas=True
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    """Запуск миграций в online-режиме."""
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        
        connectable = create_engine(
            DATABASE_URL,
            poolclass=pool.NullPool,
            pool_pre_ping=True,
            isolation_level="READ COMMITTED",
            future=True
        )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
            compare_server_default=True,
            render_as_batch=True,
            transaction_per_migration=True,
            user_module_prefix='sa.',
            include_schemas=True
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()