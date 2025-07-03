import mysql.connector

# This script streams user data from a MySQL database.
def stream_users():
    connection = None
    cursor = None
    """Generator to stream user data from the database."""
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
        cursor.execute("SELECT * FROM user_data")
        
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

           
if __name__ == "__main__":
    for user in stream_users():
        print(user)
