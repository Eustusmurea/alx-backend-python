import sqlite3
import functools

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