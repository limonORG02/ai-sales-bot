import logging
from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.core.config import settings
from app.core.bot import bot, dp
from app.api.webhook import router as telegram_router

# Настраиваем логирование, чтобы видеть, что происходит
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- ДЕЙСТВИЯ ПРИ ЗАПУСКЕ ---
    webhook_url = f"{settings.WEBHOOK_URL}/telegram/webhook"
    
    # Устанавливаем вебхук в Telegram
    await bot.set_webhook(
        url=webhook_url,
        drop_pending_updates=True, # Удаляет сообщения, пришедшие пока бот был выключен
        allowed_updates=["message", "callback_query"] # Какие типы событий ловим
    )
    logger.info(f"🚀 Бот запущен! Вебхук установлен на: {webhook_url}")
    
    yield
    
    # --- ДЕЙСТВИЯ ПРИ ОСТАНОВКЕ ---
    await bot.delete_webhook()
    await bot.session.close()
    logger.info("🛑 Бот остановлен, сессия закрыта.")

app = FastAPI(
    title=settings.PROJECT_NAME,
    version="1.0.0",
    lifespan=lifespan
)

# Подключаем роутер телеграма
app.include_router(telegram_router, prefix="/telegram", tags=["Telegram"])

@app.get("/health", tags=["System"])
async def health_check():
    return {
        "status": "ok",
        "project": settings.PROJECT_NAME
    }
