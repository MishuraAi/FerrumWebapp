# /bot/config.py

import os
from dotenv import load_dotenv

# Загружаем переменные окружения из файла .env (для локальной разработки)
load_dotenv()

# --- Блок с основными настройками ---

# Токен вашего бота
BOT_TOKEN = os.getenv("BOT_TOKEN")

# ID бригадиров (через запятую в .env)
# Преобразуем строку в список чисел
raw_brigadier_ids = os.getenv("BRIGADIER_IDS", "")
BRIGADIER_IDS = [int(id) for id in raw_brigadier_ids.split(',') if id.strip()]

# ID оператора 1С
OPERATOR_1C_ID = int(os.getenv("OPERATOR_1C_ID", 0))

# ID канала для отправки фото
TELEGRAM_CHANNEL_ID = int(os.getenv("TELEGRAM_CHANNEL_ID", 0))

# URL веб-приложения, который мы получим позже
WEB_APP_URL = os.getenv("WEB_APP_URL")


# --- Блок для работы с Google API ---

# ID вашей Google-таблицы
SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")

# ID общего диска Google Drive
GOOGLE_DRIVE_FOLDER_ID = os.getenv("GOOGLE_DRIVE_FOLDER_ID")

# Содержимое credentials.json (в виде одной строки в .env)
# Этот файл будет создан динамически при запуске на Render
# Для локального запуска просто положите credentials.json рядом
GOOGLE_CREDENTIALS_JSON_CONTENT = os.getenv("CREDENTIALS_JSON")


# --- Блок для подключения к Redis ---

# URL для подключения к Redis (берется из Render)
REDIS_URL = os.getenv("REDIS_URL")