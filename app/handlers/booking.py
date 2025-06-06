from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove, FSInputFile, BufferedInputFile
from aiogram.fsm.context import FSMContext
import aiosqlite
from app.config import ADMIN_ID
from app.services.states import BookingStates
from app.services.save_appointment import save_appointment
import csv
from io import StringIO, BytesIO
from datetime import datetime

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
    if message.from_user.id != ADMIN_ID:
        await message.answer("⚠️ У вас нет доступа к этой команде.")
        return
    
    async with aiosqlite.connect("appointments.db") as db:
        async with db.execute("SELECT * FROM appointments") as cursor:
            rows = await cursor.fetchall()
    
    if not rows:
        await message.answer("Записей пока нет.")
        return

    text = "\n".join([f"📅{id}. {date} в {time} — {name}" for id, date, time, name in rows])
    await message.answer(f"<b>Список записей:</b>\n{text}")


@router.message(F.text.startswith("/удалить "))
async def delete_appointment(message: Message):
    if message.from_user.id != ADMIN_ID:
        await message.answer("⚠️ У вас нет доступа к этой команде.")
        return

    try:
        appointment_id = int(message.text.split()[1])
    except (IndexError, ValueError):
        await message.answer("❌ Неверный формат команды. Используйте: /удалить <id>")
        return

    import aiosqlite
    async with aiosqlite.connect("appointments.db") as db:
        cursor = await db.execute("DELETE FROM appointments WHERE id = ?", (appointment_id,))
        await db.commit()

    if cursor.rowcount == 0:
        await message.answer(f"❌ Запись с id={appointment_id} не найдена.")
    else:
        await message.answer(f"✅ Запись с id={appointment_id} успешно удалена.")

@router.message(F.text == "/экспорт")
async def export_appointments(message: Message):
    if message.from_user.id != ADMIN_ID:
        await message.answer("⚠️ У вас нет доступа к этой команде.")
        return

    import aiosqlite
    async with aiosqlite.connect("appointments.db") as db:
        async with db.execute("SELECT id, date, time, name FROM appointments") as cursor:
            rows = await cursor.fetchall()

    if not rows:
        await message.answer("Записей пока нет для экспорта.")
        return

    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(["id", "date", "time", "name"])
    writer.writerows(rows)
    output.seek(0)

    byte_stream = BytesIO(output.getvalue().encode("utf-8"))
    file = BufferedInputFile(byte_stream.read(), filename=f"{datetime.now()}.csv")

    await message.answer_document(
        file,
        caption="📎 Экспорт записей"
    )
