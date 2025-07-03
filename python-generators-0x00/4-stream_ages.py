import mysql.connector

def stream_user_ages():
    """Generator to stream user ages from the database."""
    connection = None
    cursor = None
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='alx',
            password='Popote_412!',
            database='ALX_prodev'
        )
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT age FROM user_data")

        for row in cursor:
            if row['age'] is not None:  # Skip NULL ages
                yield int(row['age'])
    except mysql.connector.Error as e:
        print(f"Database error: {e}")
        raise
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

def compute_average_age():
        
        total_age = 0
        count = 0

        for age in stream_user_ages():
            total_age += age
            count += 1

        if count > 0:
            average_age = total_age / count
            print(f"Average age: {average_age:.2f}")
        else:
            print("No user data available to compute average age.")

if __name__ == "__main__":
    compute_average_age()