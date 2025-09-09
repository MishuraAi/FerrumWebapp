
# /bot/services/google_api.py

import os
import json
import gspread
from datetime import datetime
from google.oauth2.service_account import Credentials

from bot.config import SPREADSHEET_ID, GOOGLE_CREDENTIALS_JSON_CONTENT

# Определяем права доступа (scopes)
# https://docs.gspread.org/en/latest/oauth2.html#for-bots-using-service-account
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file"
]

# --- Инициализация клиента ---

def get_gspread_client():
    """
    Инициализирует и возвращает клиент gspread для работы с Google-таблицами.
    Использует учетные данные из переменных окружения.
    """
    if not GOOGLE_CREDENTIALS_JSON_CONTENT:
        raise ValueError("Отсутствует содержимое credentials.json в переменных окружения.")

    # gspread ожидает учетные данные из файла, поэтому мы создаем его динамически
    creds_dict = json.loads(GOOGLE_CREDENTIALS_JSON_CONTENT)
    creds = Credentials.from_service_account_info(creds_dict, scopes=SCOPES)
    client = gspread.authorize(creds)
    return client

# --- Основная функция ---

def add_report_to_sheet(user_id: int, user_name: str, data: dict):
    """
    Добавляет данные отчета в Google-таблицу.

    Args:
        user_id: ID пользователя Telegram.
        user_name: Имя пользователя Telegram.
        data: Словарь с данными из веб-формы.
    
    Returns:
        True, если операция прошла успешно, иначе False.
    """
    try:
        client = get_gspread_client()
        spreadsheet = client.open_by_key(SPREADSHEET_ID)
        
        # Выбираем первый лист в таблице
        worksheet = spreadsheet.sheet1

        # Форматируем данные для записи
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        department = data.get('department', 'Не указан')
        process = data.get('process', 'Не указан')
        description = data.get('description', 'Нет')
        problems = data.get('problems', 'Нет')
        
        # Преобразуем список материалов в строку для удобства записи
        materials_list = data.get('materials', [])
        materials_str = ""
        if materials_list:
            materials_str = "; ".join([f"{m.get('name', 'N/A')}: {m.get('length', 'N/A')} мм" for m in materials_list])
        else:
            materials_str = "Нет"

        # Собираем строку для добавления
        new_row = [
            timestamp,
            user_id,
            user_name,
            department,
            process,
            description,
            problems,
            materials_str
        ]

        # Добавляем новую строку в конец таблицы
        worksheet.append_row(new_row)
        
        # Проверяем заголовок таблицы и добавляем его, если лист пуст
        if worksheet.row_count == 1:
            headers = [
                "Дата и время", "ID пользователя", "Имя пользователя", "Цех", 
                "Процесс", "Описание работы", "Проблемы/Простои", "Списание металла"
            ]
            worksheet.insert_row(headers, 1)

        return True

    except gspread.exceptions.SpreadsheetNotFound:
        print(f"Ошибка: Таблица с ID '{SPREADSHEET_ID}' не найдена.")
        return False
    except Exception as e:
        print(f"Произошла ошибка при записи в Google-таблицу: {e}")
        return False

