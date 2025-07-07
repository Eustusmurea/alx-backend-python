import functools
import sqlite3

query_cache = {}

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

def cache_query(func):
    """Decorator to cache the results of a query."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # args[0] = conn, args[1] = query
        query = args[1] if len(args) > 1 else kwargs.get('query')
        if query in query_cache:
            print(f"Cache hit for query: {query}")
            return query_cache[query]
        
        print(f"Cache miss for query: {query}. Executing...")
        result = func(*args, **kwargs)
        query_cache[query] = result
        return result
    return wrapper

@with_db_connection()
@cache_query
def fetch_users_with_cache(conn, query):
    """Fetch users from the database."""
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

# Run
users = fetch_users_with_cache(query="SELECT * FROM users")
print(users)

users_again = fetch_users_with_cache(query="SELECT * FROM users")
print(users_again)  # Should hit the cache
