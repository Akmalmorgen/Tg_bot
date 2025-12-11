import asyncio
from telegram.ext import Application, CommandHandler, MessageHandler, filters

from config.settings import TOKEN
from db.database import init_db
from handlers import (
    register_start_handlers,
    register_menu_handlers,
    register_anon_link_handlers,
    register_anon_chat_handlers,
    register_roulette_handlers,
    register_admin_handlers,
    register_broadcast_handlers
)

import logger.logger as logger


async def main():
    """Главная точка запуска бота"""
    logger.info("Бот запускается...")

    # Инициализация базы данных
    await init_db()

    # Создаём приложение Telegram
    application = Application.builder().token(TOKEN).build()

    # Регистрируем все обработчики
    register_start_handlers(application)
    register_menu_handlers(application)
    register_anon_link_handlers(application)
    register_anon_chat_handlers(application)
    register_roulette_handlers(application)
    register_admin_handlers(application)
    register_broadcast_handlers(application)

    logger.info("Бот успешно запущен!")
    await application.run_polling()


if __name__ == "__main__":
    asyncio.run(main())
