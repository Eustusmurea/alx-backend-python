import sqlite3

class DatabaseConnection:

    def __init__(self, db_path='logging.db'):
        self.db_path = db_path
        self.conn = None

    def __enter__(self):
        """Establish a database connection."""
        self.conn = sqlite3.connect(self.db_path)
        return self.conn
    
    def __exit__(self, exc_type, exc_value, traceback):
        """Close the database connection."""
        if self.conn:
            self.conn.close()
        if exc_type is not None:
            print(f"An error occurred: {exc_value}")
        return False

with DatabaseConnection('logging.db') as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    results = cursor.fetchall()

    print (f"Fetched {len(results)} users:")
    