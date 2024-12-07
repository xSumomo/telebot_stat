from telegram import Update
from telegram.ext import ContextTypes
from database import create_database_and_table, add_user_and_update_message_count, update_user_rank

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.message.from_user
    chat_id = update.message.chat_id
    create_database_and_table()
    add_user_and_update_message_count(user, chat_id)
    update_user_rank(user.id, chat_id)
    await context.bot.send_message(chat_id=chat_id, text='Привет! Я бот, который отвечает на "ПРИВЕТ".')

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message and update.message.from_user:
        user = update.message.from_user
        chat_id = update.message.chat_id
        create_database_and_table()
        add_user_and_update_message_count(user, chat_id)
        update_user_rank(user.id, chat_id)
        text = update.message.text
        if text.upper() == 'ПРИВЕТ':
            await context.bot.send_message(chat_id=chat_id, text='Привет!')
