import sqlite3
import logging
import functools
import uuid

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def log_queries():
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if args:
                query = args[0]
                logging.info(f"Executing SQL query: {query}")
            return func(*args, **kwargs)
        return wrapper
    return decorator

@log_queries()
def execute_query(query, params=None):
    conn = sqlite3.connect('logging.db')
    cursor = conn.cursor()
    if params:
        cursor.execute(query, params)
    else:
        cursor.execute(query)
    conn.commit()
    conn.close()

if __name__ == "__main__":
    # Create table (if needed)
    execute_query("""
        CREATE TABLE IF NOT EXISTS users (
            user_id TEXT PRIMARY KEY,
            name TEXT,
            email TEXT,
            phone_number TEXT,
            password TEXT
        )
    """)

    # Insert with generated UUID
    user_id = str(uuid.uuid4())
    execute_query(
        "INSERT INTO users (user_id, name, email, phone_number, password) VALUES (?, ?, ?, ?, ?)",
        (user_id, 'Faith Nduta', 'faith.nduta@gmail.com', '0712345678', 'hashed_123')
    )
