# ALX Backend Python: 0x00 - Python Generators

![License](https://img.shields.io/badge/License-MIT-green)

This project is part of the **ALX Backend Specialization** and focuses on using **Python generators** to efficiently stream, batch, paginate, and aggregate data from a MySQL database. The project demonstrates memory-efficient data processing techniques for backend systems, leveraging generators to handle large datasets incrementally.

---

## Project Overview

The project consists of four tasks that implement Python generators to interact with a MySQL database (`ALX_prodev`). Each task showcases a different use case for generators:
- **Streaming**: Fetching user data row by row.
- **Batch Processing**: Processing users in batches and filtering based on conditions.
- **Lazy Pagination**: Fetching data in pages without loading the entire dataset.
- **Aggregation**: Computing aggregates (e.g., average age) efficiently.

The database contains a `user_data` table with columns: `id` (integer, primary key), `name` (varchar), `email` (varchar), and `age` (integer).

---

##  Topics Covered

- Python generators and the `yield` keyword
- Streaming data row by row from a MySQL database
- Batch processing with generators
- Lazy loading with pagination
- Memory-efficient aggregation of database data

---

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/Eustusmurea/alx-backend-python.git
cd alx-backend-python/python-generators-0x00


- **Install MySQL**: Ensure MySQL (version 8.0 or higher) is installed and running.
- **Create Database and Table**: Run the provided `seed.py` script to create the `ALX_prodev` database and `user_data` table, and load data from `user_data.csv`.




| File                       | Description                                                                 |
|----------------------------|-----------------------------------------------------------------------------|
| `seed.py`                  | Creates the `ALX_prodev` database, `user_data` table, and loads sample data  |
| `0-stream_users.py`        | Streams all users from `user_data` row by row using a generator             |
| `1-batch_processing.py`    | Streams users in batches, filtering those with `age > 25`                   |
| `2-lazy_pagination.py`     | Implements lazy pagination to fetch users in pages of specified size        |
| `3-compute_average_age.py` | Computes the average age of users, skipping NULL values                     |
| `user_data.csv`            | Sample CSV file with user data for seeding the database                     |

---

## 🚀 How to Run

Ensure the database is set up and environment variables are configured. Then run each script:

```bash
python3 0-stream_users.py
python3 1-batch_processing.py
python3 2-lazy_pagination.py
python3 3-compute_average_age.py
``` {data-source-line="90"}

---

## Key Learnings

- Using Python generators to process data lazily, reducing memory usage.
- Streaming database rows incrementally with `mysql-connector-python`.
- Implementing batch processing and pagination for scalable backend systems.
- Performing aggregations (e.g., average) without loading entire datasets into memory.
- Handling database connections and errors robustly.

---

- **Task 0**: Streams all users, printing their details.
- **Task 1**: Fetches users in batches (e.g., 5 users) and yields those with `age > 25`.
- **Task 2**: Paginates users (e.g., 5 per page) and prints each page.
- **Task 3**: Computes the average age (2 excluding NULL).

---

## Author

- **Name**: Eustus Mwirigi
- **GitHub**: [Eustusmurea](https://github.com/Eustusmurea)
- **LinkedIn**: [Eustus Mwirigi](https://www.linkedin.com/in/eustus-mwirigi/)

---

## License

This project is licensed under the [MIT License](LICENSE). It is developed for educational purposes as part of the ALX Backend Specialization.
