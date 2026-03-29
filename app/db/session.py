from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from app.core.config import settings

# Создаем асинхронный движок
engine = create_async_engine(
    settings.DATABASE_URL, 
    echo=False, # Поставь True, если захочешь видеть все SQL-запросы в терминале
    pool_pre_ping=True # Проверка соединения перед запросом
)

# Фабрика сессий
AsyncSessionLocal = async_sessionmaker(
    engine, 
    class_=AsyncSession, 
    expire_on_commit=False
)

# Зависимость (Dependency) для FastAPI, чтобы получать сессию в эндпоинтах
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
