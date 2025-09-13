# Ferrum Webapp

Проект включает в себя:
- **Bot** - Telegram бот с различными функциями
- **Webapp** - Веб-приложение с интерфейсом

## Структура проекта

```
ferapp/
├── bot/           # Telegram бот
│   ├── handlers/  # Обработчики сообщений
│   ├── keyboards/ # Клавиатуры
│   ├── logic/     # Бизнес-логика
│   ├── services/  # Сервисы
│   └── states/    # Состояния бота
├── webapp/        # Веб-приложение
│   ├── index.html
│   ├── script.js
│   └── style.css
├── requirements.txt
└── runtime.txt
```

## Установка и запуск

1. Установите зависимости:
```bash
pip install -r requirements.txt
```

2. Запустите бота:
```bash
python bot/main.py
```

3. Откройте веб-приложение в браузере:
```bash
# Откройте webapp/index.html
```

