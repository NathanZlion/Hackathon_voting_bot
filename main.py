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


from typing import Final

from telegram import User
import config
import database


from dotenv import load_dotenv
load_dotenv(".env")
BOT_TOKEN : Final = getenv("BOT_TOKEN")

router = Router()

try:
    db = database.Database()
except Exception as e:
    logging.error(f"Failed to connect to the database: {e}")
    sys.exit(1)

@router.message(CommandStart())
async def command_start(message: Message ) -> None:
    """checks if the user has already been registered in the database"""
    user = message.from_user

    if not user:
        await message.answer("Something went wrong!")
        return

    logging.log(1, user.first_name)

    await message.answer(
        f"Hi {user.full_name}, Welcome to Hackathon Voting Bot.  Please select one of the following options: ",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="Vote"), KeyboardButton(text="Projects")],
                [KeyboardButton(text="About Hackathon")],
            ],
            # q: How do I nest the buttons?
            # a: You can nest the buttons by creating a list of lists
            # q: how?
            # a: You can create a list of lists like this:
            # keyboard=[
            #     [KeyboardButton(text="Vote")],
            #     [KeyboardButton(text="Projects")],
            #     [KeyboardButton(text="About Hackathon")],
            # ],
            # q: How do I make the vote and projects buttons nested to appear side by side on the same row?
            # a: You can create a list of lists like this:
            # keyboard=[
            #     [KeyboardButton(text="Vote"), KeyboardButton(text="Projects")],

            resize_keyboard=True,
        )
    )


async def _register_user_if_not_exists(user: User):
    if not db.check_if_user_exists(user.id):
        db.add_new_user(
            user.id,
            username=user.username,
            first_name=user.first_name,
            last_name= user.last_name
        )


@router.message(F.text == "Vote")
async def register(message: Message) -> None:
    user_id = message.from_user.id

    await _register_user_if_not_exists(message.from_user)

    db.get_vote_by_user_id(user_id)

    await message.answer(
        "Please select a project to vote for",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="Project 1")],
                [KeyboardButton(text="Project 2")],
                [KeyboardButton(text="Project 3")],
                [KeyboardButton(text="Project 4")],
                [KeyboardButton(text="Project 5")],
            ],
            resize_keyboard=True,
        )
    )


@router.message(F.text == "Projects")
async def show_projects(message: Message) -> None:
    await message.answer(
        "Here are the projects",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="Project 1")],
                [KeyboardButton(text="Project 2")],
                [KeyboardButton(text="Project 3")],
                [KeyboardButton(text="Project 4")],
                [KeyboardButton(text="Project 5")],
            ],
            resize_keyboard=True,
        )
    )


@router.message(F.text == "About Hackathon")
async def about_hackathon(message: Message) -> None:
    await message.answer(
        "This is a hackathon bot"
    )


# for any think that starts with Project and a number
@router.message(F.text.startswith("Project"))
async def vote_for_project(message: Message) -> None:
    project = message.text

    user_id = message.from_user.id

    db.add_new_vote(user_id, project)

    await message.answer(
        f"Your vote for {project} has been registered"
    )


@router.message(F.text == "retract")
async def retract_vote(message: Message) -> None:
    user_id = message.from_user.id

    db.retract_vote(user_id)

    await message.answer(
        "Your vote for has been retracted"
    )


async def main():
    bot = Bot(token=BOT_TOKEN, ParseMode=ParseMode.HTML)
    dp = Dispatcher()

    dp.include_router(router)

    await dp.start_polling(bot)

if __name__ == "__main__":
    # Set up logging
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )
    asyncio.run(main())
