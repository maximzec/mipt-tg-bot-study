import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackContext, filters
from router import Router
from database import create_tables


router = Router()
create_tables()

# Логирование
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('Привет! Я помогу вам вести бюджет. Просто отправьте мне свои доходы и расходы.')


async def handle_message(update: Update, context: CallbackContext) -> None:
    user_text = update.message.text
    user_id = update.message.from_user.id
    analysis_result = router.route(user_text, user_id)
    await update.message.reply_text(f"{analysis_result}")


def main() -> None:
    # Создание приложения
    application = ApplicationBuilder().token(
        "7822050234:AAFXStKHH8x29aQB3XzORa3ZS0CJA5FtQT0").build()

    # Добавление обработчиков
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(
        filters.TEXT & ~filters.COMMAND, handle_message))

    # Запуск бота
    application.run_polling()


if __name__ == '__main__':
    main()
