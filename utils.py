from telegram import Update
from telegram.ext import ContextTypes
from database import get_top_5_users, get_top_10_users


async def top5(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.message.chat_id
    top_users = get_top_5_users(chat_id)
    if top_users:
        response = "Топ-10 пользователей:\n"
        top_user_id = top_users[0][0]  # user_id пользователя с наибольшим количеством сообщений
        second_user_id = top_users[1][0] if len(top_users) > 1 else None  # user_id пользователя на втором месте
        third_user_id = top_users[2][0] if len(top_users) > 2 else None  # user_id пользователя на третьем месте

        for i, (user_id, username, first_name, last_name, total_messages, total_experience, rank) in enumerate(top_users, start=1):
            user_display_name = username if username else f"{first_name}"
            if user_id == top_user_id:
                user_display_name = "🥇 " + user_display_name
            elif user_id == second_user_id:
                user_display_name = "🥈 " + user_display_name
            elif user_id == third_user_id:
                user_display_name = "🥉 " + user_display_name
            response += f"{i}. {user_display_name} ({rank}): {total_messages} сообщений, {total_experience} опыта\n"
        await context.bot.send_message(chat_id=chat_id, text=response)
    else:
        await context.bot.send_message(chat_id=chat_id, text="Нет данных для отображения.")



async def top_rank(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.message.chat_id
    top_users = get_top_10_users(chat_id)
    if top_users:
        response = "Топ-10 пользователей по опыту:\n"
        for i, (user_id, username, first_name, last_name, total_experience, rank) in enumerate(top_users, start=1):
            user_display_name = username if username else f"{first_name} {last_name}"
            response += f"{i}. {user_display_name} ({rank}): {total_experience} опыта\n"
        await context.bot.send_message(chat_id=chat_id, text=response)
    else:
        await context.bot.send_message(chat_id=chat_id, text="Нет данных для отображения.")