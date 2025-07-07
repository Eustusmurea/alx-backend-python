import sqlite3
import functools
import uuid

def with_db_connection(db_path='logging.db'):
    """Decorator to manage database connection."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            conn = sqlite3.connect(db_path)
            try:
                result = func(conn, *args, **kwargs)
                return result
            finally:
                conn.close()
        return wrapper
    return decorator

def transactional(func):
    """Decorator to manage transactions: commit on success, rollback on failure."""
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        try:
            result = func(conn, *args, **kwargs)
            conn.commit()
            return result
        except Exception as e:
            conn.rollback()
            print(f"Transaction failed: {e}")
            raise
    return wrapper

@with_db_connection()
@transactional
def update_user_email(conn, user_id, new_email):
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET email = ? WHERE user_id = ?", (new_email, user_id))
    print(f"Updated user {user_id}'s email to {new_email}")

