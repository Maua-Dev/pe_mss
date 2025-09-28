# import psycopg2
# import os
# from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock

# DB_NAME = "mydatabase"
# DB_USER = "myuser"
# DB_PASS = "mypassword"
# DB_HOST = "localhost"
# DB_PORT = "5432"

# def setup_postgres_table():
#     conn = None
#     try:
#         print("Connecting to PostgreSQL database...")
#         conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST, port=DB_PORT, client_encoding='utf-8')
#         cursor = conn.cursor()

#         print("Creating 'users' table if it doesn't exist...")
#         cursor.execute("""
#             CREATE TABLE IF NOT EXISTS users (
#                 user_id VARCHAR(255) PRIMARY KEY,
#                 name VARCHAR(255) NOT NULL,
#                 email VARCHAR(255) UNIQUE NOT NULL,
#                 ra VARCHAR(50),
#                 role VARCHAR(50),
#                 state VARCHAR(50),
#                 active VARCHAR(50),
#                 course VARCHAR(50),
#                 year INTEGER,
#                 organization VARCHAR(50)
#             );
#         """)
#         conn.commit()
#         print("'users' table configured successfully.")

#     except psycopg2.OperationalError as e:
#         print(f"Connection error: {e}. Please check if the PostgreSQL container is running.")
#     except Exception as e:
#         print(f"Unexpected error in setup_postgres_table: {e}")
#     finally:
#         if conn:
#             conn.close()

# def load_mock_to_postgres():
#     repo_mock = UserRepositoryMock()
#     conn = None
#     try:
#         print("\nConnecting to PostgreSQL to load mock data...")
#         conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST, port=DB_PORT, client_encoding='utf8')
#         cursor = conn.cursor()

#         print("Cleaning 'users' table...")
#         cursor.execute("TRUNCATE TABLE users RESTART IDENTITY;")
#         conn.commit()

#         print(f"Loading {len(repo_mock.users)} mock users...")
        
#         insert_query = """
#             INSERT INTO users (user_id, name, email, ra, role, state, active, course, year, organization)
#             VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
#         """
        
#         users_to_insert = []
#         for user in repo_mock.users:
#             users_to_insert.append((
#                 user.user_id,
#                 user.name,
#                 user.email,
#                 user.ra,
#                 user.role.value if user.role else None,
#                 user.state.value if user.state else None,
#                 user.active.value if user.active else None,
#                 user.course.value if user.course else None,
#                 user.year,
#                 user.organization.value if user.organization else None
#             ))
        
#         cursor.executemany(insert_query, users_to_insert)
#         conn.commit()
        
#         print(f"{cursor.rowcount} users were inserted successfully!")

#     except psycopg2.OperationalError as e:
#         print(f"Connection error: {e}. Please check if the PostgreSQL container is running.")
#     except Exception as e:
#         print(f"Unexpected error in load_mock_to_postgres: {e}")
#     finally:
#         if conn:
#             conn.close()

# if __name__ == '__main__':
#     setup_postgres_table()
#     load_mock_to_postgres()
#     print("\nLocal setup process completed.")