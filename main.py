import logging
import asyncio
import sys

import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, constants
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    CallbackQueryHandler,
)

from os import getenv


from typing import Final

from telegram import User
import config
import constant
import database
from dotenv import load_dotenv

load_dotenv(".env")

try:
    db = database.Database()
except Exception as e:
    logging.error(f"Failed to connect to the database: {e}")
    sys.exit(1)

async def _register_user_if_not_exists(user: User):
    if not db.check_if_user_exists(user.id):
        db.add_new_user(
            user.id,
            username=user.username,
            first_name=user.first_name,
            last_name= user.last_name
        )


def is_user_admin(update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
    # check if this is from a message or callback
    if update.callback_query:
        return update.callback_query.from_user.id in config.admin_ids

    return update.message.from_user.id in config.admin_ids

async def votes_status_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.callback_query.from_user
    await context.bot.delete_message(
        chat_id=update.effective_chat.id,
        message_id=update.callback_query.message.message_id
    )

    await _register_user_if_not_exists(user)

    if not user:
        await  context.bot.send_message(text="Something went wrong!")
        return

    
    if not is_user_admin(update, context):
        await context.bot.send_message(
            text="You are not authorized to view the voting status. Only admins can view the voting status",
        )
        await _send_main_menu(update, context)
        return

    text = "Voting Status : Closed \n" if constant.VOTE_CLOSED else "Voting Status : Open \n"

    for project in constant.projects:
        text += f"{project['name']} : {db.get_votes_by_project_id(project['id'])} \n"
    
    text += " Total Votes : " + str(db.get_total_votes())


    await _send_main_menu(update, context, text)

async def _send_projects_list_with_votes(update: Update, context: ContextTypes.DEFAULT_TYPE, message : str | None = None) -> None:

    await context.bot.delete_message(
        chat_id=update.effective_chat.id,
        message_id=update.callback_query.message.message_id
    )
    user = update.callback_query.from_user
    if not user:
        await context.bot.send_message("Something went wrong!")
        return

    await _register_user_if_not_exists(user)

    voted_project = db.get_vote_by_user_id(user.id)
    keyboard = []

    for project in constant.projects:
        text = project["name"]

        # tick symbol
        if voted_project is not None and project["id"] == voted_project["project_id"]:
            text += " ✅"
        else:
            text += "  "
    
        keyboard.append([InlineKeyboardButton(text, callback_data=f'vote|{project["id"]}')])
    
    keyboard.append([InlineKeyboardButton("Back", callback_data="back")])

    reply_markup = InlineKeyboardMarkup(keyboard)

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text= message or constant.PROJECTS_MESSAGE,
        reply_markup=reply_markup,
        parse_mode=constants.ParseMode.HTML
    )

async def _register_vote(user_id: User , project_id: str) -> None:
    db.add_new_vote(user_id, project_id)

""" callback data : vote|{project_id} """
async def vote_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    _user = update.callback_query.from_user
    await _register_user_if_not_exists(_user)

    project_id = update.callback_query.data.split("|")[1]
    voted_project =  db.get_vote_by_user_id(_user.id)
    db.retract_vote(_user.id)

    message = ""
    project_name = None
    # search for the name of project where id is project_id
    for project in constant.projects:
        if project["id"] == project_id:
            project_name = project["name"]
    
    if project_name == None:
        reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("Back", callback_data="back")]])

        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=text,
            reply_markup=reply_markup,
            parse_mode=constants.ParseMode.HTML
        )

    if not voted_project is None and project_id == voted_project["project_id"]:
        message += "Vote Retracted for " + project_name
    else:
        message += "Vote Registered for " + project_name
        await _register_vote(
            _user.id,
            project_id
        )
    
    text = f"{constant.THANKYOU_FOR_VOTING} {message}"
    
    await _send_projects_list_with_votes(update, context, message=text)


async def vote_menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await _register_user_if_not_exists(update.callback_query.from_user)

    if constant.VOTE_CLOSED:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Voting is closed!",
            parse_mode=constants.ParseMode.HTML
        )
        return

    text = "Please select a project to vote for."

    await _send_projects_list_with_votes(update, context, message=text)


""" callback data : projects """
async def projects_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await _register_user_if_not_exists(update.callback_query.from_user)

    text = constant.PROJECTS_MESSAGE
    keyboard = []

    await context.bot.delete_message(
        chat_id=update.effective_chat.id,
        message_id=update.callback_query.message.message_id
    )

    for project in constant.projects:
        keyboard.append([InlineKeyboardButton(project["name"], callback_data=f'project_detail|{project["id"]}')])
    
    keyboard.append([InlineKeyboardButton("Back", callback_data="back")])

    reply_markup = InlineKeyboardMarkup(keyboard)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=text,
        reply_markup=reply_markup,
        parse_mode=constants.ParseMode.HTML
    )


""" callback data : project_detail|{project_id} """
async def project_detail_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await _register_user_if_not_exists(update.callback_query.from_user)

    project_id = update.callback_query.data.split("|")[1]

    project_text = "Detail for " + project_id

    keyboard = [
        [InlineKeyboardButton("Vote", callback_data=f"vote|{project_id}")],
        [InlineKeyboardButton("Back", callback_data="back")],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=project_text,
        reply_markup=reply_markup,
        parse_mode=constants.ParseMode.HTML
    )


""" callback data : about_hackathon """
async def about_hackathon_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.delete_message(
        chat_id=update.effective_chat.id,
        message_id=update.callback_query.message.message_id
    )

    await _register_user_if_not_exists(update.callback_query.from_user)

    keyboard = [
        [InlineKeyboardButton("Visit Our Website", url="https://hackathon.a2sv.org")],
        [InlineKeyboardButton("Back", callback_data="back")],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=constant.ABOUT_HACKATHON_MESSAGE,
        reply_markup=reply_markup,
        parse_mode=constants.ParseMode.HTML
    )



""" callback data : back """
async def back_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.delete_message(
        chat_id=update.effective_chat.id,
        message_id=update.callback_query.message.message_id
    )
    
    await _register_user_if_not_exists(update.callback_query.from_user)
    reply_markup = await _send_main_menu(update, context)

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=constant.START_MESSAGE,
        reply_markup=reply_markup,
        parse_mode=constants.ParseMode.HTML
    )

async def _send_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
            [InlineKeyboardButton("Vote", callback_data="vote_menu")],
            [InlineKeyboardButton("Projects", callback_data="projects")],
            [InlineKeyboardButton("About Hackathon", callback_data="about_hackathon")],
    ]

    if is_user_admin(update, context):
        keyboard.append([InlineKeyboardButton("Status", callback_data="status")])

    reply_markup = InlineKeyboardMarkup(keyboard)
    return reply_markup

async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    if not user:
        await context.bot.send_message("🤖 Something went wrong! 🤖")
        return

    text_message = f"👋 Hi {user.full_name}\n" + constant.START_MESSAGE
    reply_markup = await _send_main_menu(update, context)
    
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=text_message,
        reply_markup=reply_markup,
        parse_mode=constants.ParseMode.HTML
    )
    await _register_user_if_not_exists(user)

if __name__ == "__main__":
    # Set up logging
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )
    TOKEN : Final = getenv("BOT_TOKEN")
    PORT : Final = getenv("PORT") or "8000"
    WEBHOOK_URL = getenv("WEBHOOK_URL")

    application = ApplicationBuilder().token(TOKEN).build()

    # Add handlera
    _start_handler = CommandHandler("start", start_handler)
    _projects_handler = CallbackQueryHandler(projects_handler, pattern="projects")
    _project_detail_handler = CallbackQueryHandler(project_detail_handler, pattern="^project_detail")
    _vote_menu_handler = CallbackQueryHandler(vote_menu_handler, pattern="^vote_menu")
    _vote_handler = CallbackQueryHandler(vote_handler, pattern="^vote")
    _back_handler = CallbackQueryHandler(back_handler, pattern="^back")
    _about_hackathon_handler = CallbackQueryHandler(about_hackathon_handler, pattern="^about_hackathon")
    _status_hackathon_handler = CallbackQueryHandler(votes_status_handler, pattern="^status")

    application.add_handler(_start_handler)
    application.add_handler(_projects_handler)
    application.add_handler(_vote_menu_handler)
    application.add_handler(_project_detail_handler)
    application.add_handler(_vote_handler)
    application.add_handler(_back_handler)
    application.add_handler(_about_hackathon_handler)
    application.add_handler(_status_hackathon_handler)
    
    application.run_webhook(
        # localhost
        listen="0.0.0.0",
        port=PORT,
        webhook_url=WEBHOOK_URL,
        allowed_updates=Update.ALL_TYPES
    )
