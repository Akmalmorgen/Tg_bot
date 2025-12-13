import asyncio

from telegram.ext import Application

from config.settings import TOKEN
from logger.logger import setup_logger
from db.database import init_db
from handlers import register_all_handlers


async def main():
    # логирование
    setup_logger()

    # база данных
    await init_db()

    # приложение
    application = Application.builder().token(TOKEN).build()

    # регистрация всех обработчиков
    register_all_handlers(application)

    # запуск
    await application.run_polling()


if __name__ == "__main__":
    asyncio.run(main())
