
from logging.config import fileConfig
import os
import sys

from alembic import context
from sqlalchemy import engine_from_config, pool
from dotenv import load_dotenv

# Đưa thư mục backend vào Python path
BACKEND_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)
ROOT_DIR = os.path.abspath(
    os.path.join(BACKEND_DIR, "..")
)

sys.path.insert(0, BACKEND_DIR)

# Đọc cấu hình từ file .env ở thư mục gốc
load_dotenv(os.path.join(ROOT_DIR, ".env"))

from app.database import Base
import app.models

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

database_url = os.getenv("DATABASE_URL")

if not database_url:
    raise RuntimeError("DATABASE_URL chưa được cấu hình trong file .env")

config.set_main_option(
    "sqlalchemy.url",
    database_url.replace("%", "%%")
)

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")

    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
