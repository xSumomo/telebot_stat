from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from telegram import Update
from handlers import start, handle_message
from utils import top5
from config import TELEGRAM_TOKEN
import logging

# Создаем форматтер для логов
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Создаем обработчик для записи логов в файл
file_handler = logging.FileHandler('bot.log')
file_handler.setFormatter(formatter)

# Настройка корневого логгера для записи всех сообщений в файл
root_logger = logging.getLogger()
root_logger.setLevel(logging.INFO)

# Удаляем все существующие обработчики у корневого логгера
if root_logger.hasHandlers():
    root_logger.handlers.clear()

# Добавляем обработчик файла к корневому логгеру
root_logger.addHandler(file_handler)

# Настройка логирования для httpx
httpx_logger = logging.getLogger("httpx")
httpx_logger.setLevel(logging.WARNING)  # Установите уровень логирования на WARNING или выше

# Удаляем все существующие обработчики у логгера httpx
if httpx_logger.hasHandlers():
    httpx_logger.handlers.clear()

# Добавляем обработчик файла к логгеру httpx
httpx_logger.addHandler(file_handler)

# Функция для обработки ошибок
async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logging.error(f"Ошибка при обработке обновления {update}: {context.error}")

def main() -> None:
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("top5", top5))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Регистрация обработчика ошибок
    application.add_error_handler(error_handler)

    application.run_polling()

if __name__ == '__main__':
    main()
