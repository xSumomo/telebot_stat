from telegram import Update
from telegram.ext import ContextTypes
from database import create_database_and_table, add_user_and_update_message_count

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.message.from_user
    chat_id = update.message.chat_id
    chat_name = update.message.chat.title if update.message.chat.title else 'No Title'
    create_database_and_table(chat_id, chat_name)
    add_user_and_update_message_count(user, chat_id, chat_name)
    await context.bot.send_message(chat_id=chat_id, text='Привет! Я бот, который отвечает на "ПРИВЕТ".')

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.message.from_user
    chat_id = update.message.chat_id
    chat_name = update.message.chat.title if update.message.chat.title else 'No Title'
    create_database_and_table(chat_id, chat_name)
    add_user_and_update_message_count(user, chat_id, chat_name)
    text = update.message.text
    if text.upper() == 'ПРИВЕТ':
        await context.bot.send_message(chat_id=chat_id, text='Привет!')
