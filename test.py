import sqlite3

DATABASE_NAME = 'bot_database.db'

def create_tables():
    # Connect to the SQLite database (or create it if it doesn't exist)
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    # Create the 'users' table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            first_name TEXT,
            last_name TEXT,
            language TEXT
        )
    ''')

    # Create the 'conversations' table with an 'id' column
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            file_name TEXT
        )
    ''')

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_tables()
