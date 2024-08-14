import logging
import asyncio
import sys

from os import getenv
from aiogram import Bot, Dispatcher, F, Router, html
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import (
    KeyboardButton,
    Message,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)

from dotenv import load_dotenv
from utils.db_handler import DB_Handler
from typing import Final


load_dotenv(".env")
BOT_TOKEN : Final = getenv("BOT_TOKEN")

router = Router()

try:
    db_handler = DB_Handler()
except:
    exit()

class Form(StatesGroup):
    name = State()
    phone_number = State()
    role = State()

@router.message(CommandStart())
async def command_start(message: Message ) -> None:
    """checks if the user has already been registered in the database"""
    user = message.from_user

    if not user:
        await message.answer("Something went wrong!")
        return

    logging.log(1, user.first_name)

    await message.answer(
        f"Hi {user.full_name}, Welcome back to Hackathon Voting Bot.",
        reply_markup=ReplyKeyboardRemove()
    )


async def main():
    bot = Bot(token=BOT_TOKEN, ParseMode=ParseMode.HTML)
    dp = Dispatcher()

    dp.include_router(router)

    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
