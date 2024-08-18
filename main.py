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
import constant
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
    user = message.from_user
    _register_user_if_not_exists(message.from_user)

    if not user:
        await message.answer("Something went wrong!")
        return

    await message.answer(
        f"Hi {user.full_name}, Welcome to Hackathon Voting Bot.  Please select one of the following options: ",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="Vote"), KeyboardButton(text="Projects")],
                [KeyboardButton(text="About Hackathon"), KeyboardButton(text="Status")],
            ],
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


@router.message(F.text == "Back")
async def back(message: Message) -> None:
    _register_user_if_not_exists(message.from_user)
    user = message.from_user

    if not user:
        await message.answer("Something went wrong!")
        return

    await message.answer(
        f"Hi {user.full_name}, Welcome to Hackathon Voting Bot.  Please select one of the following options: ",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="Vote"), KeyboardButton(text="Projects")],
                [KeyboardButton(text="About Hackathon"), KeyboardButton(text="Status")],
            ],
            resize_keyboard=True,
        )
    )


@router.message(F.text == "Vote")
async def register(message: Message) -> None:
    user_id = message.from_user.id

    await _register_user_if_not_exists(message.from_user)

    project = db.get_vote_by_user_id(user_id)
    
    print(project["project_id"] if project else "None")
    print(constant.projects[1]["name"])
    text = "Please select a project to vote for."
    if project:
        text = f"You have already voted for {project['project_id']}, Only vote if you want to change your vote."
    
    keyboard = []
    keyboard.append([KeyboardButton(text="Back")])
    for i in range(0, len(constant.projects) - 1, 2):
        keyboard.append([
            KeyboardButton(text= constant.projects[i]["name"]),
            KeyboardButton(text= constant.projects[i + 1]["name"])
        ])

    await message.answer(
        text=text,
        reply_markup=ReplyKeyboardMarkup(
            keyboard=keyboard,
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
    await message.answer("""
        🚀 Welcome to the A2SV Expo Bot! 🚀
We're thrilled to have you here! 🌍✨

What can you do?
🔍 Explore A2SV:
Learn more about A2SV, its mission, and find important links. Discover how we're empowering African tech talent and fostering innovation.

🏆 Project Voting:
Vote for your favorite projects at the A2SV Expo! Your input helps recognize outstanding work. Select "Vote for Projects" to get started.

🗣 Give Feedback:
Share your thoughts on the expo and projects. Your feedback is invaluable! Select "Give Feedback" to tell us about your experience.

Gear up for an electrifying adventure of innovation and teamwork! 🌟🚀"""
    )


# for any think that starts with Project and a number
@router.message(F.text.startswith("Project"))
async def vote_for_project(message: Message) -> None:
    project = message.text

    # validate the project
    if project not in [project["name"] for project in constant.projects]:
        await message.answer("Invalid project")
        return

    user_id = message.from_user.id

    project_id = db.get_vote_by_user_id(user_id)
    
    db.retract_vote(user_id)
    db.add_new_vote(user_id, project)

    await message.answer(
        
        f""" 🎉 Your vote for {project} has been registered! 🎉 \n
        Thank you! 🙏🏽
        """ if project_id != project else f"Your vote for {project_id} has retracted and you have voted for {project} instead",

        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text="Back"),
                ]
            ],
            resize_keyboard=True,
        )
    )


@router.message(F.text == "retract")
async def retract_vote(message: Message) -> None:
    user_id = message.from_user.id

    db.retract_vote(user_id)

    await message.answer(
        "Your vote for has been retracted"
    )

def _is_voting_open():
    return True

@router.message(F.text == "Status")
async def voting_status(message: Message) -> None:
    user = message.from_user
    if not user.id in config.admin_ids:
        await message.answer("You are not authorized to view the voting status. Only admins can view the voting status")
        return 

    text = "Voting Status : Open \n" if _is_voting_open() else "Voting Status : Closed \n"

    for project in constant.projects:
        text += f"{project['name']} : {db.get_votes_by_project_id(project['name'])} \n"
    
    text += "Total Votes : " + str(db.get_total_votes())
    
    await message.answer(text)


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
