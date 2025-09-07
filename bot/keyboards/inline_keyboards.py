# /bot/keyboards/inline_keyboards.py

from aiogram import Bot
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo, BotCommand, BotCommandScopeDefault

from bot.config import WEB_APP_URL

# --- Основная клавиатура ---
def main_keyboard():
    """Создает основную клавиатуру с кнопкой для сдачи отчета."""
    web_app_button = InlineKeyboardButton(
        text="📝 Сдать отчет",
        web_app=WebAppInfo(url=WEB_APP_URL)
    )
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[web_app_button]]
    )
    return keyboard

# --- Меню с командами (кнопка "Меню" в чате) ---
async def set_main_menu(bot: Bot):
    """Устанавливает основное меню команд для бота."""
    main_menu_commands = [
        BotCommand(command='/start', description='▶️ Запустить бота'),
        # Сюда можно будет добавить другие команды, например /help
    ]
    await bot.set_my_commands(main_menu_commands, BotCommandScopeDefault())