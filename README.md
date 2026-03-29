# 🍋 AI Sales Bot (Uzbekistan Edition)

Интеллектуальный ИИ-продавец для Telegram, адаптированный под рынок Узбекистана. Бот работает на базе **Llama 3.3 (Groq)**, поддерживает мультиязычность (RU/UZ) и обладает "зрением" для анализа фотографий товаров.

## 🚀 Основные фишки
- **Двуязычность:** Автоматическое переключение между русским и узбекским языками.
- **RAG (Knowledge Base):** Бот знает ваш прайс, акции и условия из файла `knowledge.txt`.
- **Vision Capabilities:** Анализ изображений и скриншотов от клиентов через Groq Vision.
- **Харизма:** Уникальный стиль общения "бро-консультант" с пасхалками для технарей (Arch Linux, Vim).
- **Скорость:** Интеграция с Groq API обеспечивает ответ менее чем за 1 секунду.

## 🛠 Технологический стек
- **Backend:** Python 3.14 + FastAPI
- **Database:** PostgreSQL + pgvector (для будущего поиска по эмбеддингам)
- **Migrations:** Alembic
- **Infrastructure:** Docker Compose
- **AI Engine:** Groq API (Llama 3.3 & LLaVA)
- **Telegram API:** python-telegram-bot

## ⚙️ Установка и запуск

### 1. Клонирование репозитория
```bash
git clone [https://github.com/your-username/ai-sales-bot.git](https://github.com/your-username/ai-sales-bot.git)
cd ai-sales-bot
```
### 2. Настройка окружения
Создайте файл .env и заполните его:
```
POSTGRES_USER=postgres
POSTGRES_PASSWORD=super_secret_password_123
POSTGRES_DB=ai_sales_db
POSTGRES_HOST=localhost
POSTGRES_PORT=5432

TELEGRAM_BOT_TOKEN=ваш_токен
OPENAI_API_KEY=ваш_ключ_groq
WEBHOOK_URL=[https://ваш-туннель.loca.lt](https://ваш-туннель.loca.lt)
```
### 3. Запуск через Docker
```Bash
sudo docker compose up -d
```
### 4. Применение миграций
```Bash
alembic upgrade head
```
### 5. Запуск сервера
```Bash
python -m uvicorn app.main:app --reload
```
## 📂 Структура базы знаний
Все знания бота хранятся в data/knowledge.txt. Бот использует этот файл как единственный источник правды (Single Source of Truth) для цен и акций.

## 🛡 Лицензия

MIT. "I use Arch BTW" 🍋


---
