#!/bin/bash

# Выход при любой ошибке
set -o errexit

# Устанавливаем зависимости
pip install -r requirements.txt

# Запускаем Gunicorn, который будет управлять Uvicorn
# Он запускает FastAPI-приложение, находящееся в файле bot/main.py
gunicorn -w 4 -k uvicorn.workers.UvicornWorker bot.main:app --bind 0.0.0.0:$PORT