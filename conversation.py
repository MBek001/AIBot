import os
import sqlite3
from datetime import datetime

# Directory to save conversations
CONVERSATIONS_DIR = "conversations"

def save_user_info(user_id, username, first_name, last_name):
    conn = sqlite3.connect('bot_database.db')
    cursor = conn.cursor()
    cursor.execute('''
    INSERT OR REPLACE INTO users (user_id, username, first_name, last_name)
    VALUES (?, ?, ?, ?)
    ''', (user_id, username, first_name, last_name))
    conn.commit()
    conn.close()

def get_conversation_file_name(user_id):
    conn = sqlite3.connect('bot_database.db')
    cursor = conn.cursor()
    cursor.execute('''
    SELECT file_name FROM conversations WHERE user_id = ? ORDER BY id DESC LIMIT 1
    ''', (user_id,))
    file_name = cursor.fetchone()
    conn.close()

    if file_name:
        return file_name[0]
    return None

def save_conversation_record(user_id, file_name):
    conn = sqlite3.connect('bot_database.db')
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO conversations (user_id, file_name)
    VALUES (?, ?)
    ''', (user_id, file_name))
    conn.commit()
    conn.close()

def save_conversation_to_file(user_id, messages):
    # Determine the filename based on user_id and current date
    date_str = datetime.now().strftime("%Y-%m-%d")
    file_name = f"{user_id}_{date_str}.txt"
    file_path = os.path.join(CONVERSATIONS_DIR, file_name)

    # Append messages to the file
    with open(file_path, "a") as file:
        for sender, message in messages:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            file.write(f"{timestamp} {sender}: {message}\n")

    return file_name

def load_conversation_from_file(user_id):
    date_str = datetime.now().strftime("%Y-%m-%d")
    file_name = f"{user_id}_{date_str}.txt"
    file_path = os.path.join(CONVERSATIONS_DIR, file_name)

    conversation_history = []
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            conversation_history = file.readlines()

    return conversation_history
