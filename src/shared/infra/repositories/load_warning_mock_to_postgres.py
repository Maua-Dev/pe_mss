import psycopg2
import os
from src.shared.infra.repositories.warning_repository_mock import WarningRepositoryMock

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
    
def setup_warning_tables(cursor):
    """Cria as tabelas relacionadas a Warnings se não existirem."""
    
    print("Ensuring 'users' table exists for foreign key dependency...")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id VARCHAR(255) PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) UNIQUE NOT NULL,
            role VARCHAR(50)
            -- Outras colunas de user...
        );
    """)
    
    print("Creating 'warnings' related tables...")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS warnings (
            warning_id VARCHAR(36) PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            description TEXT,
            expire TIMESTAMPTZ NOT NULL,
            viewed BOOLEAN NOT NULL DEFAULT FALSE
        );
        
        CREATE TABLE IF NOT EXISTS user_warning (
            user_id VARCHAR(255) NOT NULL,
            warning_id VARCHAR(36) NOT NULL,
            PRIMARY KEY (user_id, warning_id),
            FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
            FOREIGN KEY (warning_id) REFERENCES warnings(warning_id) ON DELETE CASCADE
        );
        
        CREATE TABLE IF NOT EXISTS role_warning (
            role VARCHAR(50) NOT NULL,
            warning_id VARCHAR(36) NOT NULL,
            PRIMARY KEY (role, warning_id),
            FOREIGN KEY (warning_id) REFERENCES warnings(warning_id) ON DELETE CASCADE
        );
    """)
    print("Warning tables configured successfully.")


def load_mock_warnings(cursor):
    """Limpa e carrega os dados mockados de warnings."""
    print("\nCleaning warning related tables...")
    cursor.execute("TRUNCATE TABLE warnings, user_warning, role_warning RESTART IDENTITY;")

    repo_mock = WarningRepositoryMock()
    print(f"Loading {len(repo_mock.warnings)} mock warnings...")
    warning_insert_query = "INSERT INTO warnings (warning_id, title, description, expire, viewed) VALUES (%s, %s, %s, %s, %s)"
    warnings_to_insert = [
        (w.warning_id, w.title, w.description, w.expire, w.viewed)
        for w in repo_mock.warnings
    ]
    cursor.executemany(warning_insert_query, warnings_to_insert)
    
    print(f"Loading {len(repo_mock.user_warning)} user-warning links...")
    uw_insert_query = "INSERT INTO user_warning (user_id, warning_id) VALUES (%s, %s)"
    uw_to_insert = [(link.user_id, link.warning_id) for link in repo_mock.user_warning]
    cursor.executemany(uw_insert_query, uw_to_insert)

    print(f"Loading {len(repo_mock.role_warning)} role-warning links...")
    rw_insert_query = "INSERT INTO role_warning (role, warning_id) VALUES (%s, %s)"
    rw_to_insert = [(link.role.value, link.warning_id) for link in repo_mock.role_warning]
    cursor.executemany(rw_insert_query, rw_to_insert)
    
    print("\nMock data for warnings loaded successfully!")

if __name__ == '__main__':
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        setup_warning_tables(cursor)
        load_mock_warnings(cursor)
        
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