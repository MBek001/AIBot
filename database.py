import os
import sqlite3
from datetime import datetime

# Directory to save conversations
CONVERSATIONS_DIR = "conversations"

# Create the directory if it does not exist
if not os.path.exists(CONVERSATIONS_DIR):
    os.makedirs(CONVERSATIONS_DIR)


def initialize_db():
    conn = sqlite3.connect('bot_database.db')
    cursor = conn.cursor()

    # Create users table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        username TEXT,
        first_name TEXT,
        last_name TEXT,
        language TEXT
    )
    ''')

    # Create conversations table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS conversations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        file_name TEXT,
        FOREIGN KEY (user_id) REFERENCES users (user_id)
    )
    ''')

    conn.commit()
    conn.close()


def save_user_info(user_id, username, first_name, last_name, language=None):
    conn = sqlite3.connect('bot_database.db')
    cursor = conn.cursor()
    cursor.execute('''
    INSERT OR REPLACE INTO users (user_id, username, first_name, last_name, language)
    VALUES (?, ?, ?, ?, ?)
    ''', (user_id, username, first_name, last_name, language))
    conn.commit()
    conn.close()


def get_user_info(user_id):
    conn = sqlite3.connect('bot_database.db')
    cursor = conn.cursor()
    cursor.execute('''
    SELECT first_name FROM users WHERE user_id = ?
    ''', (user_id,))
    user_info = cursor.fetchone()
    conn.close()

    return user_info[0] if user_info else None


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


initialize_db()
