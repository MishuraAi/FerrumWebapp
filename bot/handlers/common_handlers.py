# /bot/handlers/common_handlers.py

from aiogram import Router, types
from aiogram.filters import CommandStart

# Пока создадим "пустую" клавиатуру, наполним ее в следующем шаге
from bot.keyboards.inline_keyboards import main_keyboard

# Создаем роутер для этих обработчиков
router = Router()

@router.message(CommandStart())
async def cmd_start(message: types.Message):
    """
    Обработчик команды /start.
    Приветствует пользователя и показывает основную клавиатуру.
    """
    user_name = message.from_user.full_name
    await message.answer(
        f"Здравствуйте, {user_name}!\n\n"
        "Я бот для сдачи и учета производственных отчетов.",
        reply_markup=main_keyboard() # Прикрепляем клавиатуру к сообщению
    )