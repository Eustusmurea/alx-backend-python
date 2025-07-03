import mysql.connector



def stream_users_in_batches(batch_size):
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

        cursor = connection.cursor(dictionary=True)

        offset = 0

        while True:
            cursor.execute (
                "SELECT * FROM user_data LIMIT %s OFFSET %s",
                (batch_size, offset)
            )

            batch = cursor.fetchall()
            if not batch:
                break

            for row in batch:
                row['age'] = int(row['age'])

            yield batch
            offset += batch_size

        cursor.close()
        connection.close()
    except mysql.connector.Error as err:
        print(f"Error: {err}")


def batch_processing(batch_size):
    for batch in stream_users_in_batches(batch_size):
        for user in batch:
            if user['age'] > 25:
                yield user

if __name__ == "__main__":
    for user in batch_processing(5):
        print(user)

            