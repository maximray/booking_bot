import aiosqlite

async def save_appointment(date: str, time: str, name: str):
    async with aiosqlite.connect("appointments.db") as db:
        await db.execute(
            "INSERT INTO appointments (date, time, name) VALUES (?, ?, ?)",
            (date, time, name)
        )
        await db.commit()
