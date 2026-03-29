import asyncio
import os
import sys
from logging.config import fileConfig

from alembic import context
from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config

# 1. Добавляем корневую директорию в системные пути Python
# Это нужно, чтобы Alembic "видел" папку app и твои настройки
sys.path.insert(0, os.path.realpath(os.path.join(os.path.dirname(__file__), '..')))

# 2. Импортируем твои настройки и метаданные моделей
from app.core.config import settings
from app.db.base import Base
# Импортируем модели, чтобы Alembic видел их при --autogenerate
from app.models.client import Client 

# Объект конфигурации Alembic
config = context.config

# 3. Принудительно подставляем URL из твоего .env (игнорируем alembic.ini)
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

# Настройка логирования
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Указываем метаданные для автоматического создания миграций
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Запуск миграций в 'offline' режиме (без подключения к БД)."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    """Вспомогательная функция для выполнения миграций."""
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online() -> None:
    """Запуск миграций в 'online' режиме (асинхронно)."""

    # --- БЛОК ОТЛАДКИ (DEBUG) ---
    print("\n" + "="*60)
    print("🚀 ПРОВЕРКА ПОДКЛЮЧЕНИЯ К БАЗЕ:")
    print(f"🔗 URL: {settings.DATABASE_URL}")
    print("="*60 + "\n")
    # ----------------------------

    # Создаем асинхронный движок
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        # Поскольку Alembic синхронный, мы используем run_sync
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
