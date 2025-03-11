from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor

TOKEN = "7929304981:AAFjlQRzUBqhxwCHZYExWsvszOVhrQhJo-U"  # Вставь новый токен
ADMIN_ID = 5123513507  # Твой Telegram ID
CHANNEL_ID = -1001985807352  # ID канала для отзывов
DONATION_LINK = "https://www.tinkoff.ru/rm/r_yuwsPPGJXh.XjAAbtmNYY/OHkG163677"  # Ссылка на донаты

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# Кнопки главного меню
main_menu = InlineKeyboardMarkup(row_width=1)
btn_feedback = InlineKeyboardButton("📝 Задать анонимный вопрос, написать отзыв", callback_data="feedback")
btn_donate = InlineKeyboardButton("💰 Поддержать проекты Лукавой", callback_data="donate")
main_menu.add(btn_feedback, btn_donate)

# Обработчик команды /start
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer("Привет! Выбери действие:", reply_markup=main_menu)

# Обработчик нажатия кнопок
@dp.callback_query_handler(lambda c: c.data in ["feedback", "donate"])
async def process_callback(callback_query: types.CallbackQuery):
    if callback_query.data == "feedback":
        await bot.send_message(callback_query.from_user.id, "Напиши сообщение, я передам его Лукавой:")
    elif callback_query.data == "donate":
        await bot.send_message(callback_query.from_user.id, f"💰 Поддержать проект можно здесь: {DONATION_LINK}")

# Обработчик отзывов
@dp.message_handler()
async def handle_feedback(message: types.Message):
    if message.chat.type == "private":  # Только личные сообщения
        feedback_text = f"📩 Новый отзыв от @{message.from_user.username}:\n\n{message.text}"
        
        # Отправляем отзыв админу
        await bot.send_message(ADMIN_ID, feedback_text)
        
        # Отправляем отзыв в канал
        await bot.send_message(CHANNEL_ID, feedback_text)
        
        await message.answer("Спасибо за отзыв! 💜")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
