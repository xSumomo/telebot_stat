import sqlite3
from datetime import datetime

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
