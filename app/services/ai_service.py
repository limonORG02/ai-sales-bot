from openai import AsyncOpenAI
from app.core.config import settings
from app.models.client import FunnelStatus
from app.services.rag_service import RAGService

class AIService:
    def __init__(self):
        # Подключаемся к Groq
        self.client = AsyncOpenAI(
            base_url="https://api.groq.com/openai/v1", 
            api_key=settings.OPENAI_API_KEY.get_secret_value()
        )
        # Используем мощную модель Llama 3.3
        self.model = "llama-3.3-70b-versatile"
        self.rag = RAGService()

    async def get_sale_response(self, message_text: str, client_status: FunnelStatus, first_name: str) -> str:
        try:
            # Загружаем базу знаний (цены в сумах, акции, пасхалки)
            knowledge = self.rag.get_knowledge_context()

            system_prompt = f"""
            Ты — мультиязычный бро-консультант из команды Лимона. Работаешь на рынке Узбекистана.
            Твоя цель: продавать ИИ-решения, общаясь как живой человек, а не робот.

            ЯЗЫКОВАЯ ПОЛИТИКА:
            - Если клиент пишет на узбекском — отвечай на узбекском (используй уважительное 'Siz', но в стиле 'aka/do'stim').
            - Если клиент пишет на русском — отвечай на русском (стиль 'бро', уважително если клиент пишет 'Вы' а еслы у него тоже не уважителная монера можно переходит на 'бро' ).
            - На каком языке обратились, на том и отвечай. Если смешивают (узрус) — делай так же.

            ПРАВИЛА ОБЩЕНИЯ:
            1. НЕ ЗДОРОВАЙСЯ повторно. Если диалог идет — сразу к сути.
            2. Пиши кратко, максимум 2-3 абзаца.
            3. Используй цены в сумах (so'm) и акции из БАЗЫ ЗНАНИЙ.
            4. Не забывай про харизму и Arch Linux/Vim пасхалки, если в тему.

            БАЗА ЗНАНИЙ:
            {knowledge}

            ДАННЫЕ КЛИЕНТА:
            Имя: {first_name}
            Этап воронки: {client_status.value}
            """

            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": message_text}
                ],
                temperature=0.8,
                max_tokens=800
            )
            return response.choices[0].message.content

        except Exception as e:
            # Если что-то пошло не так, выводим ошибку в консоль и даем нейтральный ответ
            print(f"❌ ОШИБКА AI SERVICE: {e}")
            return "Брат, что-то связь лагает. Повтори еще раз, или я сейчас Лимона позову."
