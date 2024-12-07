from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from telegram import Update
from handlers import start, handle_message
from utils import top5
from config import TELEGRAM_TOKEN
import logging

# Настройка логирования в файл
logging.basicConfig(
    filename='bot.log',  # Имя файла для логирования
    filemode='a',  # Режим записи в файл (a - добавление)
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.WARNING
)

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
