from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.fsm.strategy import FSMStrategy
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.client.default import DefaultBotProperties
from aiogram.filters.command import Command

from app.handlers import booking
from app.config import BOT_TOKEN
from app.db.init_db import init_db

import logging

logging.basicConfig(level=logging.INFO)

# Создаём бота и диспетчер
bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher(storage=MemoryStorage(), fsm_strategy=FSMStrategy.CHAT)

@dp.message(Command("start"))
async def cmd_start(message: Message):
    builder = InlineKeyboardBuilder()
    builder.button(text="📅 Записаться", callback_data="book_appointment")
    await message.answer(
        "Привет! Я бот для записи на приём.\nНажмите кнопку ниже, чтобы выбрать дату:",
        reply_markup=builder.as_markup()
    )

if __name__ == "__main__":
    import asyncio

    dp.include_router(booking.router)
    async def main():
        await init_db()
        await dp.start_polling(bot)

    asyncio.run(main())
