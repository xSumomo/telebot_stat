import sqlite3
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from datetime import datetime

# Замените 'YOUR_TOKEN_HERE' на токен, который вы получили от @BotFather
TOKEN = '5845145624:AAFANaFDXMLjebfO-rVdAuiXO_j4NYqLQic'

# Имя базы данных SQLite
DB_NAME = 'test-db.db'

# Функция для создания базы данных и таблицы пользователей для конкретного чата
def create_database_and_table(chat_id, chat_name):
    # Преобразование chat_id в строку и замена недопустимых символов
    table_name = f't_{chat_id}'.replace('-', '_').replace(':', '_').replace('@', '_')
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    try:
        cursor.execute(f'''
            CREATE TABLE IF NOT EXISTS {table_name} (
                user_id INTEGER,
                username TEXT,
                first_name TEXT,
                last_name TEXT,
                chat_name TEXT,
                date TEXT,
                message_count INTEGER DEFAULT 0,
                PRIMARY KEY (user_id, date)
            )
        ''')
        conn.commit()
        print(f"База данных и таблица пользователей для чата {chat_id} созданы или уже существуют.")
    except sqlite3.Error as e:
        print(f"Ошибка при создании базы данных или таблицы для чата {chat_id}: {e}")
    finally:
        conn.close()

# Функция для добавления пользователя в базу данных и обновления количества сообщений
def add_user_and_update_message_count(user, chat_id, chat_name):
    # Преобразование chat_id в строку и замена недопустимых символов
    table_name = f't_{chat_id}'.replace('-', '_').replace(':', '_').replace('@', '_')
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    try:
        # Получение текущей даты
        current_date = datetime.now().strftime('%Y-%m-%d')

        cursor.execute(f'''
            INSERT OR IGNORE INTO {table_name} (user_id, username, first_name, last_name, chat_name, date, message_count)
            VALUES (?, ?, ?, ?, ?, ?, 0)
        ''', (user.id, user.username, user.first_name, user.last_name, chat_name, current_date))
        conn.commit()
        print(f"Пользователь {user.username} добавлен в базу данных или уже существует.")

        cursor.execute(f'''
            UPDATE {table_name}
            SET message_count = message_count + 1
            WHERE user_id = ? AND date = ?
        ''', (user.id, current_date))
        conn.commit()
        print(f"Количество сообщений для пользователя {user.username} обновлено.")
    except sqlite3.Error as e:
        print(f"Ошибка при добавлении пользователя или обновлении количества сообщений: {e}")
    finally:
        conn.close()

# Функция для получения топ-5 пользователей по количеству сообщений
def get_top_5_users(chat_id):
    table_name = f't_{chat_id}'.replace('-', '_').replace(':', '_').replace('@', '_')
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    try:
        cursor.execute(f'''
            SELECT user_id, username, first_name, last_name, SUM(message_count) as total_messages
            FROM {table_name}
            GROUP BY user_id
            ORDER BY total_messages DESC
            LIMIT 5
        ''')
        top_users = cursor.fetchall()
        return top_users
    except sqlite3.Error as e:
        print(f"Ошибка при получении топ-5 пользователей: {e}")
    finally:
        conn.close()



async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.message.from_user
    chat_id = update.message.chat_id
    chat_name = update.message.chat.title if update.message.chat.title else 'No Title'
    create_database_and_table(chat_id, chat_name)
    add_user_and_update_message_count(user, chat_id, chat_name)
    text = update.message.text
    if text.upper() == 'ПРИВЕТ':
        await update.message.reply_text('Привет!')

async def top5(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.message.chat_id
    top_users = get_top_5_users(chat_id)
    if top_users:
        response = "Топ-5 пользователей по количеству сообщений:\n"
        top_user_id = top_users[0][0]  # user_id пользователя с наибольшим количеством сообщений
        for i, (user_id, username, first_name, last_name, total_messages) in enumerate(top_users, start=1):
            user_display_name = username if username else f"{first_name}"
            if user_id == top_user_id:
                user_display_name += " ⭐"
            response += f"{i}. {user_display_name}: {total_messages} сообщений\n"
        await update.message.reply_text(response)
    else:
        await update.message.reply_text("Нет данных для отображения.")

def main() -> None:
    application = ApplicationBuilder().token(TOKEN).build()

    application.add_handler(CommandHandler("top5", top5))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    application.run_polling()

if __name__ == '__main__':
    main()
