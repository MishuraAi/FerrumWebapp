# /bot/handlers/report_handlers.py

import json
from aiogram import Router, F, types

# Импортируем нашу новую функцию для работы с Google-таблицами
from bot.services.google_api import add_report_to_sheet

router = Router()

@router.message(F.web_app_data)
async def web_app_data_handler(message: types.Message):
    """
    Обработчик данных, полученных от Web App.
    """
    # Распаковываем данные из JSON-строки
    data = json.loads(message.web_app_data.data)
    
    # Пытаемся сохранить данные в Google-таблицу
    success = add_report_to_sheet(
        user_id=message.from_user.id,
        user_name=message.from_user.full_name,
        data=data
    )

    if success:
        # Формируем позитивный ответ
        response_text = "✅ **Отчет успешно сохранен!**\n\n"
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
    else:
        # Формируем сообщение об ошибке
        response_text = (
            "❌ **Произошла ошибка!**\n\n"
            "Не удалось сохранить ваш отчет. Пожалуйста, попробуйте еще раз.\n"
            "Если проблема повторится, обратитесь к администратору."
        )

    await message.answer(response_text)
