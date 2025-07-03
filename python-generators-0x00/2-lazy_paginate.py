import mysql.connector

def paginate_users(page_size, offset):
    """Generator to paginate user data from the database."""
    connection = None
    cursor = None
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='alx',
            password='Popote_412!',
            database='ALX_prodev'
        )

        """ Check if the connection was successful """
        if connection.is_connected():
            print("Connected to the database.")
        else:
            print("Failed to connect to the database.")
            return
        """ Create a cursor to execute queries """
        cursor = connection.cursor(dictionary=True)
        cursor.execute(
            "SELECT * FROM user_data LIMIT %s OFFSET %s",
            (page_size, offset)
        )
        
        for row in cursor:
            row['age'] = int(row['age'])
            yield row
    except mysql.connector.Error as e:
        print(f"Database error: {e}")
        raise
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
    
def lazy_paginate(page_size):
        """Generator to lazily paginate user data."""
        offset = 0
        while True:
            page = paginate_users(page_size, offset)
            if not page:
                break
            yield page
            offset += page_size

if __name__ == "__main__":
    for page in lazy_paginate(5):
        print(page)
        for user in page:
            print(user)
            