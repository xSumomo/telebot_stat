import sqlite3
from datetime import datetime
import random
import logging

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.WARNING
)

# Имя базы данных SQLite
DB_NAME = 'test-db.db'

# Функция для создания базы данных и таблицы пользователей
def create_database_and_table():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    try:
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS main_data_user (
                user_id INTEGER,
                chat_id INTEGER,
                username TEXT,
                first_name TEXT,
                last_name TEXT,
                date TEXT,
                message_count INTEGER DEFAULT 0,
                experience INTEGER DEFAULT 0,
                rank TEXT DEFAULT 'Новичок',
                PRIMARY KEY (user_id, chat_id, date)
            )
        ''')
        conn.commit()
        logging.info("Таблица main_data_user создана или уже существует.")
    except sqlite3.Error as e:
        logging.error(f"Ошибка при создании базы данных или таблицы: {e}")
    finally:
        conn.close()

# Функция для добавления пользователя в базу данных и обновления количества сообщений и опыта
def add_user_and_update_message_count(user, chat_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    try:
        # Получение текущей даты
        current_date = datetime.now().strftime('%Y-%m-%d')

        # Генерация случайного количества опыта
        experience = random.randint(1, 10)

        cursor.execute('''
            INSERT OR IGNORE INTO main_data_user (user_id, chat_id, username, first_name, last_name, date, message_count, experience, rank)
            VALUES (?, ?, ?, ?, ?, ?, 0, 0, 'Новичок')
        ''', (user.id, chat_id, user.username, user.first_name, user.last_name, current_date))
        conn.commit()
        logging.info(f"Пользователь {user.username} добавлен в базу данных или уже существует.")

        cursor.execute('''
            UPDATE main_data_user
            SET message_count = message_count + 1, experience = experience + ?
            WHERE user_id = ? AND chat_id = ? AND date = ?
        ''', (experience, user.id, chat_id, current_date))
        conn.commit()
        logging.info(f"Количество сообщений и опыт для пользователя {user.username} обновлены.")

        # Обновление звания пользователя
        update_user_rank(user.id, chat_id)
    except sqlite3.Error as e:
        logging.error(f"Ошибка при добавлении пользователя или обновлении количества сообщений и опыта: {e}")
    finally:
        conn.close()

# Функция для обновления звания пользователя
def update_user_rank(user_id, chat_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    try:
        cursor.execute('''
            SELECT SUM(experience) as total_experience
            FROM main_data_user
            WHERE user_id = ? AND chat_id = ?
        ''', (user_id, chat_id))
        total_experience = cursor.fetchone()[0]

        new_rank = 'Новичок'
        if total_experience >= 500:
            new_rank = 'ЛЕГЕНДА'
        elif total_experience >= 400:
            new_rank = 'ГУРУ'
        elif total_experience >= 300:
            new_rank = 'ЧЕХОТКА'
        elif total_experience >= 200:
            new_rank = 'САДИСТ'

        cursor.execute('''
            UPDATE main_data_user
            SET rank = ?
            WHERE user_id = ? AND chat_id = ?
        ''', (new_rank, user_id, chat_id))
        conn.commit()
        logging.info(f"Звание пользователя {user_id} в чате {chat_id} обновлено на {new_rank}.")
    except sqlite3.Error as e:
        logging.error(f"Ошибка при обновлении звания пользователя: {e}")
    finally:
        conn.close()

# Функция для получения топ-10 пользователей по количеству сообщений
def get_top_10_users(chat_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    try:
        cursor.execute('''
            SELECT user_id, username, first_name, last_name, SUM(message_count) as total_messages, SUM(experience) as total_experience, rank
            FROM main_data_user
            WHERE chat_id = ?
            GROUP BY user_id
            ORDER BY total_messages DESC
            LIMIT 10
        ''', (chat_id,))
        top_users = cursor.fetchall()
        return top_users
    except sqlite3.Error as e:
        logging.error(f"Ошибка при получении топ-10 пользователей: {e}")
    finally:
        conn.close()

# Функция для получения топ-5 пользователей по количеству сообщений
def get_top_5_users(chat_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    try:
        cursor.execute('''
            SELECT user_id, username, first_name, last_name, SUM(message_count) as total_messages, SUM(experience) as total_experience, rank
            FROM main_data_user
            WHERE chat_id = ?
            GROUP BY user_id
            ORDER BY total_messages DESC
            LIMIT 10
        ''', (chat_id,))
        top_users = cursor.fetchall()
        return top_users
    except sqlite3.Error as e:
        logging.error(f"Ошибка при получении топ-5 пользователей: {e}")
    finally:
        conn.close()