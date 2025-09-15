import psycopg2
import os
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock

DB_NAME = "mydatabase"
DB_USER = "myuser"
DB_PASS = "mypassword"
DB_HOST = "localhost"
DB_PORT = "5432"

def get_db_connection():
    """Função centralizada para obter uma conexão com o banco"""
    return psycopg2.connect(
        dbname=DB_NAME, user=DB_USER, password=DB_PASS,
        host=DB_HOST, port=DB_PORT, client_encoding='utf-8'
    )
    
def setup_user_tables(cursor):
    
    print("Creating 'users' table...")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id VARCHAR(255) PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) UNIQUE NOT NULL,
            ra VARCHAR(50),
            role VARCHAR(50),
            state VARCHAR(50),
            active VARCHAR(50),
            course VARCHAR(50),
            year INTEGER,
            organization VARCHAR(50)
        );
    """)
    
    print("Users tables configured successfully.")


def load_mock_users(cursor):
    """Limpa e carrega os dados mockados de warnings."""
    print("\nCleaning users related tables...")
    cursor.execute("TRUNCATE TABLE users RESTART IDENTITY;")

    repo_mock = UserRepositoryMock()
    print(f"Loading {len(repo_mock.users)} mock warnings...")
    
    user_insert_query = """
            INSERT INTO users (user_id, name, email, ra, role, state, active, course, year, organization)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
    
    users_to_insert = []
    for user in repo_mock.users:
        users_to_insert.append((
            user.user_id,
            user.name,
            user.email,
            user.ra,
            user.role.value if user.role else None,
            user.state.value if user.state else None,
            user.active.value if user.active else None,
            user.course.value if user.course else None,
            user.year,
            user.organization.value if user.organization else None
        ))
    
    cursor.executemany(user_insert_query, users_to_insert)
    
    print("\nMock data for users loaded successfully!")

if __name__ == '__main__':
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        setup_user_tables(cursor)
        load_mock_users(cursor)
        
        conn.commit()
        cursor.close()
        
    except psycopg2.OperationalError as e:
        print(f"Connection error: {e}. Please check if the PostgreSQL container is running.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        if conn:
            conn.rollback()
    finally:
        if conn:
            conn.close()
        print("\nWarning setup process completed.")
