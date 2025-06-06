from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
import aiosqlite
from app.services.states import BookingStates
from app.services.save_appointment import save_appointment

router = Router()

# Старт диалога после нажатия кнопки "Записаться"
@router.callback_query(F.data == "book_appointment")
async def start_booking(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(
        "Введите дату приёма (например, 6 июня):",
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(BookingStates.choosing_date)

# Получаем дату
@router.message(BookingStates.choosing_date)
async def get_date(message: Message, state: FSMContext):
    await state.update_data(date=message.text)
    await message.answer("Введите время (например, 15:00):")
    await state.set_state(BookingStates.choosing_time)

# Получаем время
@router.message(BookingStates.choosing_time)
async def get_time(message: Message, state: FSMContext):
    await state.update_data(time=message.text)
    await message.answer("Введите ваше имя:")
    await state.set_state(BookingStates.entering_name)

# Получаем имя и подтверждаем
@router.message(BookingStates.entering_name)
async def get_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    data = await state.get_data()
    date, time, name = data["date"], data["time"], data["name"]
    await save_appointment(date, time, name)

    await message.answer(
        f"✅ Вы записались на <b>{date}</b> в <b>{time}</b>\nИмя: <b>{name}</b>",
        reply_markup=ReplyKeyboardRemove()
    )
    await state.clear()

@router.message(F.text == "/записи")
async def show_appointments(message: Message):
    async with aiosqlite.connect("appointments.db") as db:
        async with db.execute("SELECT date, time, name FROM appointments") as cursor:
            rows = await cursor.fetchall()
    
    if not rows:
        await message.answer("Записей пока нет.")
        return

    text = "\n".join([f"📅 {date} в {time} — {name}" for date, time, name in rows])
    await message.answer(f"<b>Список записей:</b>\n{text}")

