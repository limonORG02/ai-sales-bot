from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.client import Client, FunnelStatus
from aiogram.types import Message

class ClientService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_or_create_client(self, event: Message) -> Client:
        """Находит клиента в базе или создает нового, если его нет."""
        tg_user = event.from_user
        
        # 1. Ищем клиента по telegram_id
        query = select(Client).where(Client.telegram_id == tg_user.id)
        result = await self.db.execute(query)
        client = result.scalar_one_or_none()

        # 2. Если не нашли — создаем
        if not client:
            client = Client(
                telegram_id=tg_user.id,
                username=tg_user.username,
                first_name=tg_user.first_name,
                status=FunnelStatus.NEW
            )
            self.db.add(client)
            await self.db.commit()
            await self.db.refresh(client)
            print(f"🆕 Создан новый клиент: {tg_user.id}")
        else:
            # 3. Если нашли — обновляем время активности (опционально username)
            client.username = tg_user.username
            await self.db.commit()
            print(f"✅ Клиент вернулся: {tg_user.id}")
            
        return client
