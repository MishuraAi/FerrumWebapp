import asyncio
import logging
import uvicorn
from fastapi import FastAPI

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.enums import ParseMode

# Импортируем наши настройки и обработчики
from bot.config import BOT_TOKEN, REDIS_URL
from bot.handlers import common_handlers, report_handlers, brigadier_handlers
from bot.keyboards.inline_keyboards import set_main_menu

# --- FastAPI app ---
# Это нужно, чтобы Render видел, что наше приложение "живое"
app = FastAPI()

@app.get("/")
def read_root():
    """Корневой эндпоинт для проверки работоспособности."""
    return {"status": "bot is running"}

# --- Aiogram Bot ---
async def main():
    """Основная функция для запуска бота."""
    # Настраиваем логирование для отладки
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s"
    )

    # Создаем объекты Бота и Диспетчера
    # В качестве хранилища состояний (FSM) используем Redis
    storage = RedisStorage.from_url(REDIS_URL)
    bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
    dp = Dispatcher(storage=storage)

    # Настраиваем главное меню бота (команды /start, /help и т.д.)
    await set_main_menu(bot)

    # Регистрируем роутеры с обработчиками
    # Важен порядок: сначала более специфичные, потом общие
    dp.include_router(common_handlers.router)
    dp.include_router(report_handlers.router)
    dp.include_router(brigadier_handlers.router)

    # Пропускаем накопившиеся апдейты и запускаем polling
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    # Это основной цикл запуска.
    # Мы запускаем веб-сервер и бота в одном асинхронном цикле.

    # Конфигурация для uvicorn
    config = uvicorn.Config(
        app="bot.main:app",  # Путь к нашему FastAPI app
        host="0.0.0.0",
        port=8000,
        loop="asyncio"
    )
    server = uvicorn.Server(config)

    # Создаем и запускаем асинхронные задачи для бота и сервера
    loop = asyncio.get_event_loop()
    bot_task = loop.create_task(main())
    server_task = loop.create_task(server.serve())

    # Запускаем обе задачи одновременно до их завершения
    try:
        loop.run_until_complete(asyncio.gather(bot_task, server_task))
    except KeyboardInterrupt:
        logging.info("Application stopped manually.")
    finally:
        loop.close()