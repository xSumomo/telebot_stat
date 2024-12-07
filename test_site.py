from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

# Имя базы данных SQLite
DB_NAME = 'test-db.db'

# Функция для получения данных из таблицы
def get_table_data(chat_id):
    # Преобразование chat_id в строку и замена недопустимых символов
    table_name = f'chat_{chat_id}'.replace('-', '_').replace(':', '_').replace('@', '_')
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    try:
        cursor.execute(f'SELECT * FROM {table_name}')
        data = cursor.fetchall()
        return data
    except sqlite3.Error as e:
        print(f"Ошибка при получении данных из таблицы {table_name}: {e}")
        return []
    finally:
        conn.close()

@app.route('/')
def index():
    # Пример chat_id, который вы хотите отобразить
    chat_id = 111  # Замените на реальный chat_id
    data = get_table_data(chat_id)
    return render_template('index.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)
