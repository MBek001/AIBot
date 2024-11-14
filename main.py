import logging
import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import ContentType
from aiogram.utils import executor
from datetime import datetime

from config import TELEGRAM_TOKEN
from utils import encode_image, analyze_image, generate_response
from conversation import save_user_info, get_conversation_file_name, save_conversation_record, save_conversation_to_file, load_conversation_from_file
from queries import dp

# Use your actual home directory for PythonAnywhere
BASE_DIR = '/home/tuya/AIBot/'

# Directory to save images and conversations
IMAGE_DIR = os.path.join(BASE_DIR, 'images')
CONVERSATIONS_DIR = os.path.join(BASE_DIR, 'conversations')

# Create the directories if they do not exist
os.makedirs(IMAGE_DIR, exist_ok=True)
os.makedirs(CONVERSATIONS_DIR, exist_ok=True)

# Set up the bot token
API_TOKEN = TELEGRAM_TOKEN
bot = Bot(token=API_TOKEN)

@dp.message_handler(content_types=[ContentType.TEXT])
async def handle_text(message: types.Message):
    user_id = message.from_user.id
    username = message.from_user.username
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name

    # Save user info to the database
    save_user_info(user_id, username, first_name, last_name)

    user_text = message.text
    # Load previous conversation history
    previous_conversation = load_conversation_from_file(user_id)
    context = "\n".join(previous_conversation) + f"\nUser: {user_text}\nAI:"

    # Generate AI response based on the context
    response_text = await generate_response(context)
    response_text = response_text.replace("User:", "").replace("AI:", "").strip()

    # Prepare messages for saving
    messages = [
        ('User', user_text),
        ('AI', response_text)
    ]

    # Get existing conversation file name
    file_name = get_conversation_file_name(user_id)

    # If no existing file, create a new one; otherwise, append to the existing one
    if file_name is None:
        file_name = save_conversation_to_file(user_id, messages)
        save_conversation_record(user_id, file_name)
    else:
        save_conversation_to_file(user_id, messages)

    await message.answer(response_text)

@dp.message_handler(content_types=ContentType.PHOTO)
async def handle_photo(message: types.Message):
    # Send initial response to let the user know the photo is being processed
    initial_message = await message.reply("Your photo is being analyzed, please wait...")

    # Download the image
    file_id = message.photo[-1].file_id
    file = await bot.get_file(file_id)
    file_path = file.file_path

    # Define the full path to save the image
    image_path = os.path.join(IMAGE_DIR, f"{message.from_user.id}_temp_image.jpg")

    # Download and save the image
    await bot.download_file(file_path, image_path)

    # Analyze the image
    analysis_result = analyze_image(image_path)

    # Prepare messages for saving
    user_id = message.from_user.id
    messages = [
        ('User', "User sent a photo."),
        ('AI', f"Analysis result: {analysis_result}")
    ]

    # Get existing conversation file name
    file_name = get_conversation_file_name(user_id)

    # If no existing file, create a new one; otherwise, append to the existing one
    if file_name is None:
        file_name = save_conversation_to_file(user_id, messages)
        save_conversation_record(user_id, file_name)
    else:
        save_conversation_to_file(user_id, messages)

    # Edit the initial message with the analysis result
    await bot.edit_message_text(
        text=f"Analysis complete:\n{analysis_result}",
        chat_id=message.chat.id,
        message_id=initial_message.message_id
    )

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(dp, skip_updates=True)
    
