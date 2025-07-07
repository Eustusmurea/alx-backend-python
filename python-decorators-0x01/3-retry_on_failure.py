import time
import functools
import sqlite3

def retry_on_failure(retries=3, delay=2):
    """Decorator to retry a function on failure."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt < retries - 1:
                        print(f"Attempt {attempt + 1} failed: {e}. Retrying in {delay} seconds...")
                        time.sleep(delay)
                    else:
                        print(f"All {retries} attempts failed.")
                        raise
        return wrapper
    return decorator

def with_db_connection(db_path='logging.db'):
    def decorator(func):
        @functools.wraps(func)
        def wrapper (*args, **kwargs):
            conn = sqlite3.connect(db_path)

            try:
                result = func(conn, *args, **kwargs)
                return result
            finally:
                conn.close()
        return wrapper
    return decorator

@with_db_connection('logging.db')
@retry_on_failure(retries=5, delay=1)
def fetch_users_with_retry(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()

users = fetch_users_with_retry()
print(users)