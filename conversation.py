import os
import sqlite3
from datetime import datetime

# Base directory for your project
BASE_DIR = '***'

# Directory to save conversations
CONVERSATIONS_DIR = os.path.join(BASE_DIR, 'conversations')

# Ensure the conversations directory exists
if not os.path.exists(CONVERSATIONS_DIR):
    try:
        os.makedirs(CONVERSATIONS_DIR, exist_ok=True)
        print(f"Created conversations directory: {CONVERSATIONS_DIR}")
    except OSError as e:
        print(f"Error creating conversations directory: {e}")

def initialize_db():
    """Initialize the database and create tables if they don't exist."""
    try:
        # Use absolute path for the database file
        db_path = os.path.join(BASE_DIR, 'bot_database.db')
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Create users table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            first_name TEXT,
            last_name TEXT
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
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    finally:
        conn.close()

def save_user_info(user_id, username, first_name, last_name):
    try:
        db_path = os.path.join(BASE_DIR, 'bot_database.db')
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute('''
        INSERT OR REPLACE INTO users (user_id, username, first_name, last_name)
        VALUES (?, ?, ?, ?)
        ''', (user_id, username, first_name, last_name))
        conn.commit()
    except sqlite3.Error as e:
        print(f"Error saving user info: {e}")
    finally:
        conn.close()

def get_conversation_file_name(user_id):
    try:
        db_path = os.path.join(BASE_DIR, 'bot_database.db')
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute('''
        SELECT file_name FROM conversations WHERE user_id = ? ORDER BY id DESC LIMIT 1
        ''', (user_id,))
        file_name = cursor.fetchone()
    except sqlite3.Error as e:
        print(f"Error retrieving conversation file name: {e}")
        return None
    finally:
        conn.close()

    return file_name[0] if file_name else None

def save_conversation_record(user_id, file_name):
    try:
        db_path = os.path.join(BASE_DIR, 'bot_database.db')
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute('''
        INSERT INTO conversations (user_id, file_name)
        VALUES (?, ?)
        ''', (user_id, file_name))
        conn.commit()
    except sqlite3.Error as e:
        print(f"Error saving conversation record: {e}")
    finally:
        conn.close()

def save_conversation_to_file(user_id, messages):
    """Saves conversation messages to a text file."""
    # Determine the filename based on user_id and current date
    date_str = datetime.now().strftime("%Y-%m-%d")
    file_name = f"{user_id}_{date_str}.txt"
    file_path = os.path.join(CONVERSATIONS_DIR, file_name)

    # Append messages to the file
    try:
        with open(file_path, "a") as file:
            for sender, message in messages:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                file.write(f"{timestamp} {sender}: {message}\n")
        print(f"Saved conversation to {file_path}")
    except IOError as e:
        print(f"Error writing to file {file_name}: {e}")

    return file_name

def load_conversation_from_file(user_id):
    """Loads conversation history from a text file."""
    date_str = datetime.now().strftime("%Y-%m-%d")
    file_name = f"{user_id}_{date_str}.txt"
    file_path = os.path.join(CONVERSATIONS_DIR, file_name)

    conversation_history = []
    if os.path.exists(file_path):
        try:
            with open(file_path, "r") as file:
                conversation_history = file.readlines()
            print(f"Loaded conversation from {file_path}")
        except IOError as e:
            print(f"Error reading file {file_name}: {e}")

    return conversation_history

# Initialize database at the start of the application
initialize_db()
