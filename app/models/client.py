import enum
from sqlalchemy import Integer, String, BigInteger, Enum, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from datetime import datetime

from app.db.base import Base

# Те самые стадии продаж из твоего ТЗ
class FunnelStatus(str, enum.Enum):
    NEW = "NEW"                 # Только начал диалог
    INTERESTED = "INTERESTED"   # Задает вопросы, смотрит варианты
    CONSIDERING = "CONSIDERING" # Сомневается, нужны аргументы
    READY = "READY"             # Готов покупать
    LEAD = "LEAD"               # Оставил контакты/оплатил

class Client(Base):
    __tablename__ = "clients"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    # Используем BigInteger, так как ID в Telegram бывают очень длинными
    telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True, index=True, nullable=False)
    
    username: Mapped[str | None] = mapped_column(String, nullable=True)
    first_name: Mapped[str | None] = mapped_column(String, nullable=True)
    phone: Mapped[str | None] = mapped_column(String, nullable=True)
    
    # Ключевое поле: статус клиента
    status: Mapped[FunnelStatus] = mapped_column(
        Enum(FunnelStatus), 
        default=FunnelStatus.NEW, 
        nullable=False
    )
    
    # Автоматические таймстемпы
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), onupdate=func.now(), nullable=True)
