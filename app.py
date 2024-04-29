import os
import asyncio
from aiogram import Dispatcher, Bot
import sqlite3 as sq
from handlers import user_private

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

bot = Bot(token=os.getenv('TOKEN'))

dp = Dispatcher()

dp.include_router(user_private)

with sq.connect("db.db") as con:
    cur = con.cursor()
    # cur.execute("DROP TABLE IF EXISTS users")
    cur.execute("""CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER,
                ENG_words TEXT,
                RUS_words TEXT,
                FIRST_word TEXT,
                SECOND_word TEXT,
                THIRD_word TEXT,
                FOURTH_word TEXT,
                FIFTH_word TEXT
    )
""")
    con.commit()


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=['message'])


asyncio.run(main())
