import logging
import os

# ===============================
# 🔹 Настройка логирования
# ===============================

LOG_FILE = "bot.log"

# Создаём логгер
logger = logging.getLogger("WhoAnonimBot")
logger.setLevel(logging.INFO)

# Формат логов
formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

# ---------- Логи в файл ----------
file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# ---------- Логи в консоль ----------
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)


def get_logger():
    """Возвращает настроенный логгер"""
    return logger
