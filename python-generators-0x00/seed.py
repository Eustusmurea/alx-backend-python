import mysql.connector
import csv
import uuid
import os
from mysql.connector import Error

DB_NAME = 'ALX_prodev'
TABLE_NAME = 'user_data'
CSV_FILE_PATH = 'user_data.csv'

def read_csv_data(file_path):
    """Read user data from a CSV file and return a list of tuples (name, email, age)."""
    try:
        with open(file_path, mode='r', encoding='utf-8') as file:
            csv_reader = csv.reader(file)
            next(csv_reader, None)  # Skip header row, if present
            return [(row[0], row[1], float(row[2])) for row in csv_reader if len(row) >= 3]
    except FileNotFoundError:
        print(f"Error: CSV file '{file_path}' not found.")
        return []
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return []

def connect_db():
    """Connect to MySQL server."""
    try:
        return mysql.connector.connect(
            host='localhost',
            user='alx',
            password='Popote_412!'
        )
    except Error as e:
        print(f"Error connecting to MySQL server: {e}")
        return None

def create_database(connection):
    """Create the database if it doesn't exist."""
    if not connection:
        return
    try:
        with connection.cursor() as cursor:
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
        connection.commit()
    except Error as e:
        print(f"Error creating database: {e}")

def connect_to_prodev():
    """Connect to the specific database."""
    try:
        return mysql.connector.connect(
            host='localhost',
            user='alx',
            password='Popote_412!',
            database=DB_NAME
        )
    except Error as e:
        print(f"Error connecting to database {DB_NAME}: {e}")
        return None

def create_table(connection):
    """Create the user_data table if it doesn't exist."""
    if not connection:
        return
    try:
        with connection.cursor() as cursor:
            cursor.execute(f"""
                CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
                    user_id CHAR(36) PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    email VARCHAR(255) NOT NULL UNIQUE,
                    age DECIMAL NOT NULL
                )
            """)
        connection.commit()
    except Error as e:
        print(f"Error creating table: {e}")

def insert_data(connection, data):
    """Insert user data into the table."""
    if not connection or not data:
        return
    try:
        with connection.cursor() as cursor:
            for row in data:
                name, email, age = row
                try:
                    # Check if email already exists
                    cursor.execute(f"""
                        SELECT user_id FROM {TABLE_NAME} WHERE email = %s
                    """, (email,))
                    if cursor.fetchone():
                        print(f"User with email {email} already exists. Skipping insert.")
                        continue

                    user_id = str(uuid.uuid4())
                    cursor.execute(f"""
                        INSERT INTO {TABLE_NAME} (user_id, name, email, age)
                        VALUES (%s, %s, %s, %s)
                    """, (user_id, name, email, age))
                except Error as err:
                    print(f"Error inserting data for {email}: {err}")
        connection.commit()
    except Error as e:
        print(f"Error during data insertion: {e}")

if __name__ == "__main__":
    # Connect to MySQL server and create database
    db_connection = connect_db()
    if db_connection:
        create_database(db_connection)
        db_connection.close()

    # Connect to the specific database and create table
    prodev_connection = connect_to_prodev()
    if prodev_connection:
        create_table(prodev_connection)

        # Read CSV data and insert into table
        user_data = read_csv_data(CSV_FILE_PATH)
        if user_data:
            insert_data(prodev_connection, user_data)
            print("Database and table created, data inserted successfully.")
        else:
            print("No data to insert.")
        prodev_connection.close()
    else:
        print("Failed to connect to the database.")