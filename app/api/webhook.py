from fastapi import APIRouter, Request, Depends
from aiogram.types import Update, Message
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.bot import bot, dp
from app.db.session import get_db
from app.services.client_service import ClientService
from app.services.ai_service import AIService # Импортируем новый сервис

router = APIRouter()
ai_service = AIService() # Инициализируем один раз

@router.post("/webhook")
async def telegram_webhook(request: Request, db: AsyncSession = Depends(get_db)):
    update_data = await request.json()
    update = Update.model_validate(update_data, context={"bot": bot})
    await dp.feed_update(bot, update, db=db)
    return {"status": "ok"}

@dp.message()
async def handle_message(message: Message, db: AsyncSession):
    # 1. Регистрация клиента в базе
    client_service = ClientService(db)
    client = await client_service.get_or_create_client(message)
    
    # 2. Отправляем статус "печатает", чтобы клиент не нервничал
    await bot.send_chat_action(chat_id=message.chat.id, action="typing")
    
    # 3. Получаем ответ от AI
    ai_response = await ai_service.get_sale_response(
        message_text=message.text,
        client_status=client.status,
        first_name=client.first_name or "Друг"
    )
    
    # 4. Отвечаем клиенту
    await message.answer(ai_response)
