# /bot/handlers/report_handlers.py

import json
from aiogram import Router, F, types

router = Router()

@router.message(F.web_app_data)
async def web_app_data_handler(message: types.Message):
    """
    Обработчик данных, полученных от Web App.
    """
    # Распаковываем данные из JSON-строки
    data = json.loads(message.web_app_data.data)
    
    # Формируем ответное сообщение
    # TODO: В будущем здесь будет логика сохранения в Google Sheets
    response_text = "✅ **Отчет получен!**\n\n"
    response_text += f"**Цех:** {data.get('department', 'Не указан')}\n"
    response_text += f"**Процесс:** {data.get('process', 'Не указан')}\n"
    response_text += f"**Описание:** {data.get('description', 'Нет')}\n"
    response_text += f"**Проблемы:** {data.get('problems', 'Нет')}\n\n"
    
    if data.get('materials'):
        response_text += "**Списание металла:**\n"
        for material in data.get('materials'):
            name = material.get('name', 'N/A')
            length = material.get('length', 'N/A')
            response_text += f"- {name}: {length} мм\n"

    await message.answer(response_text)