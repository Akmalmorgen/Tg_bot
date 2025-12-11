import asyncio
from telegram.ext import (
    Application,
    MessageHandler,
    CommandHandler,
    CallbackQueryHandler,
    filters
)

# Импортируем настройки
from config.settings import TOKEN

# Импортируем регистрацию всех хендлеров
from handlers import (
    register_start_handlers,
    register_menu_handlers,
    register_anon_link_handlers,
    register_anon_chat_handlers,
    register_roulette_handlers,
    register_admin_handlers,
    register_broadcast_handlers
)

# Подключение базы
from db.database import init_db


async def main():
    # Инициализация бота
    app = Application.builder().token(TOKEN).build()

    print("📦 Инициализация базы данных...")
    await init_db()

    print("🔗 Регистрация обработчиков...")
    register_start_handlers(app)
    register_menu_handlers(app)
    register_anon_link_handlers(app)
    register_anon_chat_handlers(app)
    register_roulette_handlers(app)
    register_admin_handlers(app)
    register_broadcast_handlers(app)

    print("🚀 Бот запущен и слушает обновления!")
    await app.run_polling()


if __name__ == "__main__":
    asyncio.run(main())
