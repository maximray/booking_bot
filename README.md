# Booking Bot

Telegram-бот для бронирования с использованием aiogram и SQLite.

## Установка

1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/maximray/booking_bot
   cd booking_bot
   ```
2. Создайте виртуальное окружение и активируйте его:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # Linux/macOS
   # или
   venv\Scripts\activate.bat # Windows
   ```
3. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```
4. Создайте .env файл на основе .env.example и заполните токен бота и айди админа

## Запуск
```bash
python3 -m app.main
```
## Структура проекта
```bash
booking_bot/
├── app/
│   ├── __init__.py             # Пустой, для признания папки модулем
│   ├── config.py              # Конфигурация через pydantic + dotenv
│   ├── main.py                # Точка входа — запуск бота
│   ├── db/
│   │   └── init_db.py         # Инициализация базы данных SQLite
│   ├── handlers/
│   │   └── booking.py         # Хендлеры aiogram для бронирования
│   └── services/
│       ├── __init__.py        # Пустой
│       ├── save_appointment.py # Логика сохранения записи в БД
│       └── states.py          # FSM состояния для диалогов
├── .env.example               # Пример env файла с переменными
├── .gitignore                 # Исключаем лишнее из репозитория
├── README.md                  # Описание проекта, инструкции
└── requirements.txt           # Зависимости для pip
```
## Зависимости
См. requirements.txt
```yaml
---

**requirements.txt**

```txt
aiofiles==24.1.0
aiogram==3.20.0.post0
aiosqlite==0.21.0
python-dotenv==1.1.0
pydantic==2.11.5
```
```
