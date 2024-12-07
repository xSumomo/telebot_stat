from database import get_top_5_users

async def top5(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None: # type: ignore
    chat_id = update.message.chat_id
    top_users = get_top_5_users(chat_id)
    if top_users:
        response = "Топ-5 пользователей по количеству сообщений:\n"
        top_user_id = top_users[0][0]  # user_id пользователя с наибольшим количеством сообщений
        for i, (user_id, username, first_name, last_name, total_messages) in enumerate(top_users, start=1):
            user_display_name = username if username else f"{first_name} {last_name}"
            if user_id == top_user_id:
                user_display_name += " ⭐"
            response += f"{i}. {user_display_name}: {total_messages} сообщений\n"
        await context.bot.send_message(chat_id=chat_id, text=response)
    else:
        await context.bot.send_message(chat_id=chat_id, text="Нет данных для отображения.")
