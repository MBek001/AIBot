import logging
import os
import sqlite3
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils import executor
from config import TELEGRAM_TOKEN
from datetime import datetime

API_TOKEN = TELEGRAM_TOKEN
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Dictionary to keep track of user language and joined date
user_language = {}
user_joined = {}

# Define the database name and the path to conversation files
DATABASE_NAME = 'bot_database.db'
CONVERSATION_FILES_PATH = 'conversations/'  # Update this path

# Function to create the keyboard markup with About and Help buttons
def help_about_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=3)  # Adjust row width as needed
    start_button = InlineKeyboardButton("Start 📌", callback_data="start")
    help_button = InlineKeyboardButton("Help 🆘", callback_data="help")
    about_button = InlineKeyboardButton("About 🔆", callback_data="about")
    account_button = InlineKeyboardButton("Account 📋", callback_data="account")

    # URL button to redirect to the owner's Telegram profile
    contact_button = InlineKeyboardButton("Contact Owner 📧", url="https://t.me/O_Mirzabek")

    # Add buttons to the keyboard
    keyboard.add(help_button, about_button, account_button, contact_button, start_button)
    return keyboard


# Function to create language selection keyboard
def language_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=2)
    uzbek_button = InlineKeyboardButton("Uzbek 🇺🇿", callback_data="lang_uz")
    english_button = InlineKeyboardButton("English 🇺🇸", callback_data="lang_en")
    russian_button = InlineKeyboardButton("Russian 🇷🇺", callback_data="lang_ru")
    keyboard.add(english_button, uzbek_button, russian_button)
    return keyboard

# Command handler for the /start command
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    user_joined[message.from_user.id] = datetime.now()  # Track when the user joined
    await message.answer("Please select your language:", reply_markup=language_keyboard())


# Callback query handler for language selection
@dp.callback_query_handler(lambda c: c.data.startswith("lang_"))
async def process_language_selection(callback_query: types.CallbackQuery):
    lang_code = callback_query.data.split("_")[1]
    languages = {
        "uz": "Uzbek",
        "en": "English",
        "ru": "Russian",
    }
    selected_language = languages.get(lang_code, "English")

    # Store the user's selected language
    user_language[callback_query.from_user.id] = selected_language

    # Send a welcome message in the selected language and remove the language selection buttons
    if selected_language == "English":
        welcome_message = (
            "Language selected: English. 🎉\n\n"
            "Here’s what you can do:\n"
            "1. Send me a text, and I will respond with some information.\n"
            "2. Send me a photo, and I will analyze it for you.\n\n"
            "Use the buttons below to get started!"
        )
    elif selected_language == "Uzbek":
        welcome_message = (
            "Siz O'zbek tilini tanladingiz! 🎉\n\n"
            "Bot nimalar qila oladi?\n"
            "1. Siz yuborgan savollarga javob beradi.\n"
            "2. Rasmlaringizni tahlil qiladi.\n\n"
            "Quyidagi tugmalar orqali botdan foydalanishni boshlang!"
        )
    elif selected_language == "Russian":
        welcome_message = (
            "Вы выбрали Русский язык! 🎉\n\n"
            "Что может сделать бот?\n"
            "1. Ответить на ваши вопросы.\n"
            "2. Проанализировать отправленные вами фотографии.\n\n"
            "Используйте кнопки ниже, чтобы начать!"
        )

    await bot.answer_callback_query(callback_query.id)
    await bot.edit_message_text(
        chat_id=callback_query.from_user.id,
        message_id=callback_query.message.message_id,
        text=welcome_message,
        reply_markup=help_about_keyboard()
    )

@dp.callback_query_handler(lambda c: c.data in ['about', 'help', 'start', 'account'])
async def process_callback_button(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    language = user_language.get(user_id, "English")  # Default to English if not set

    if callback_query.data == 'about':
        if language == "English":
            await bot.send_message(user_id, "This bot was created by Mirzabek Ochilov, a developer at Cognilabs Company.")
        elif language == "Uzbek":
            await bot.send_message(user_id, "Bu bot Cognilabs Companiyasining dasturchisi Ochilov Mirzabek tomonidan yaratildi.")
        elif language == "Russian":
            await bot.send_message(user_id, "Этот бот был создан Мирзабеком Очиловым, разработчиком компании Cognilabs.")

    elif callback_query.data == 'help':
        if language == "English":
            await bot.send_message(user_id, (
                "Here are the available commands:\n"
                "/start - Start the bot\n"
                "/account - View your account information\n"
                "/help - List all commands\n"
                "/about - Learn about the bot\n"
                "Contact Owner - Use the Contact Owner button below."
            ))
        elif language == "Uzbek":
            await bot.send_message(user_id, (
                "Quyidagi buyruqlar mavjud:\n"
                "/start - Botni boshlash\n"
                "/account - Hisobingiz haqida ma'lumot\n"
                "/help - Barcha buyruqlar\n"
                "/about - Bot haqida ma'lumot\n"
                "Egalar bilan bog'lanish uchun pastdagi tugmani ishlating."
            ))
        elif language == "Russian":
            await bot.send_message(user_id, (
                "Доступные команды:\n"
                "/start - Запустить бота\n"
                "/account - Просмотреть информацию об аккаунте\n"
                "/help - Список всех команд\n"
                "/about - Узнать о боте\n"
                "Связаться с владельцем - Используйте кнопку ниже."
            ))

    elif callback_query.data == 'start':
        if language == "English":
            await bot.send_message(user_id, "Let's get started! Send me a message or photo to begin.")
        elif language == "Uzbek":
            await bot.send_message(user_id, "Keling, boshlaymiz! Menga xabar yoki rasm yuboring.")
        elif language == "Russian":
            await bot.send_message(user_id, "Давайте начнем! Отправьте мне сообщение или фото.")

    elif callback_query.data == 'account':
        await bot.send_message(user_id, "To manage your account, type /account.")



# Command handler for the /account command
@dp.message_handler(commands=['account'])
async def account_info(message: types.Message):
    user_id = message.from_user.id
    join_date = user_joined.get(user_id, "Unknown")
    language = user_language.get(user_id, "English")

    # Create an inline keyboard with the clear history button
    clear_history_button = InlineKeyboardButton("Clear History 🗑", callback_data="clear_history")
    keyboard = InlineKeyboardMarkup().add(clear_history_button)

    # Display user information
    response = f"Language: {language}\nJoined: {join_date}\n"
    await message.answer(response, reply_markup=keyboard)

# Callback handler for clearing history
@dp.callback_query_handler(lambda c: c.data == 'clear_history')
async def clear_history(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    try:
        # Clear user cache
        await clear_user_cache(user_id)
        await bot.answer_callback_query(callback_query.id, "Your history has been cleared!")
        await bot.send_message(user_id, "Your conversation history has been successfully cleared.")
    except Exception as e:
        await bot.answer_callback_query(callback_query.id, f"Error clearing history: {e}")

async def clear_user_cache(user_id: int):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    try:
        # Fetch the user's conversation entry
        cursor.execute('SELECT file_name FROM conversations WHERE user_id = ?', (user_id,))
        file_name = cursor.fetchone()

        if file_name:
            file_path = os.path.join(CONVERSATION_FILES_PATH, file_name[0])
            if os.path.exists(file_path):
                try:
                    os.remove(file_path)
                    print(f"File {file_path} deleted successfully.")
                except Exception as e:
                    print(f"Error deleting file: {e}")

            # Remove the conversation record from the database
            cursor.execute('DELETE FROM conversations WHERE user_id = ?', (user_id,))
            conn.commit()
            print("User conversation cache cleared successfully.")
        else:
            print("No conversation found for the user.")
    except Exception as e:
        print(f"Error clearing user cache: {e}")
    finally:
        conn.close()

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(dp, skip_updates=True)
        
