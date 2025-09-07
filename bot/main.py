# /bot/main.py

import asyncio
import logging

from aiogram import Bot, Dispatcher, F
from aiogram.fsm.storage.redis import RedisStorage
from fastapi import FastAPI
import uvicorn

# Импортируем наши настройки и обработчики
from bot.config import BOT_TOKEN, REDIS_URL
from bot.handlers import common_handlers, report_handlers, brigadier_handlers
from bot.keyboards.inline_keyboards import set_main_menu


# --- FastAPI app ---
# Это нужно, чтобы Render видел, что наше приложение "живое"
app = FastAPI()

@app.get("/")
def read_root():
    return {"status": "bot is running"}


# --- Aiogram Bot ---
async def main():
    # Настраиваем логирование для отладки
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(name)s - %(message)s")

    # Создаем объекты Бота и Диспетчера
    # В качестве хранилища состояний (FSM) используем Redis
    storage = RedisStorage.from_url(REDIS_URL)
    bot = Bot(token=BOT_TOKEN, parse_mode="HTML")
    dp = Dispatcher(storage=storage)

    # Настраиваем главное меню бота (команда /start)
    await set_main_menu(bot)

    # Регистрируем роутеры с обработчиками
    # Важен порядок: сначала более специфичные, потом общие
    dp.include_router(common_handlers.router)
    # dp.include_router(report_handlers.router)    # Пока закомментируем, добавим позже
    # dp.include_router(brigadier_handlers.router) # Пока закомментируем, добавим позже

    # Пропускаем накопившиеся апдейты и запускаем polling
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    # Это основной цикл запуска
    # Мы запускаем веб-сервер и бота в одном асинхронном цикле
    
    # Конфигурация для uvicorn
    config = uvicorn.Config(
        app="bot.main:app", # Путь к нашему FastAPI app
        host="0.0.0.0",
        port=8000,
        reload=True, # Включаем авто-перезагрузку для удобства разработки
        loop="asyncio"
    )
    server = uvicorn.Server(config)

    # Создаем и запускаем асинхронные задачи
    loop = asyncio.get_event_loop()
    bot_task = loop.create_task(main())
    server_task = loop.create_task(server.serve())

    # Запускаем обе задачи одновременно
    loop.run_until_complete(asyncio.gather(bot_task, server_task))