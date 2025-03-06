from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackQueryHandler, ContextTypes
import asyncio
from telegram.error import TelegramError

# Данные админов (замени на свои)
ADMIN_CHAT_IDS = [5123513507, 123456789]  # ID чатов админов
DONATE_CARD = "https://www.tinkoff.ru/rm/r_yuwsPPGJXh.XjAAbtmNYY/OHkG163677"  # Номер карты для донатов

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Задать анонимный вопрос, написать отзыв", callback_data='ask_question')],
        [InlineKeyboardButton("Отблагодарить Лукавую", callback_data='donate')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Привет! Выбери действие:", reply_markup=reply_markup)

# Обработка анонимных вопросов
async def handle_question(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    question = update.message.text

    # Отправляем вопрос всем админам
    for admin_id in ADMIN_CHAT_IDS:
        await context.bot.send_message(
            chat_id=admin_id,
            text=f"Новый вопрос от @{user.username} (ID: {user.id}):\n\n{question}"
        )

    # Отправляем пользователю подтверждение
    await update.message.reply_text("Ваше анонимное послание отправлено Лукавой. Спасибо за обращение!😊")

# Обработка кнопок
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == 'ask_question':
        await query.message.reply_text("Напишите ваш вопрос, и мы передадим его анонимно.")
    elif query.data == 'donate':
        await query.message.reply_text(f"Спасибо за поддержку!🎉\n\nНомер карты: {DONATE_CARD}")

# Основная функция
async def main():
    # Вставь сюда свой токен
    token = '7929304981:AAFIXg2-b_pHL8Mi-qti6dRUwAcWXwjgjHU'

    # Создаем приложение
    application = Application.builder().token(token).build()

    # Регистрируем обработчики
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_question))
    application.add_handler(CallbackQueryHandler(button_handler))

    # Запускаем бота с обработкой ошибок
    while True:
        try:
            await application.run_polling()
        except TelegramError as e:
            print(f"Ошибка: {e}. Перезапуск через 5 секунд...")
            await asyncio.sleep(5)

if __name__ == '__main__':
    asyncio.run(main())
