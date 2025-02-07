import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackContext, filters
from router import Router

router = Router()


# Логирование
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('Привет! Я помогу вам вести бюджет. Просто отправьте мне свои доходы и расходы.')

async def handle_message(update: Update, context: CallbackContext) -> None:
    user_text = update.message.text
    analysis_result = router.route(user_text)
    await update.message.reply_text(f"Результат анализа: {analysis_result}")

async def total_week(update: Update, context: CallbackContext) -> None:
    # Логика для подсчета расходов за неделю
    await update.message.reply_text('Вы потратили X за последнюю неделю.')

def main() -> None:
    # Создание приложения
    application = ApplicationBuilder().token("7822050234:AAFXStKHH8x29aQB3XzORa3ZS0CJA5FtQT0").build()

    # Добавление обработчиков
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_handler(CommandHandler("total_week", total_week))

    # Запуск бота
    application.run_polling()

if __name__ == '__main__':
    main() 