import psycopg2
import psycopg2.extras

class PostgresTestDatasource:

    def __init__(self):
        self.connection_params = {
            "dbname": "mydatabase",
            "user": "myuser",
            "password": "mypassword",
            "host": "localhost",
            "port": "5432"
        }

    def query(self, sql, params):
        query_psycopg2 = sql
        param_keys = params.keys()
        for key in param_keys:
            query_psycopg2 = query_psycopg2.replace(f":{key}", "%s")
       
        params_tuple = tuple(params.values())

        conn = None
        try:
            conn = psycopg2.connect(**self.connection_params)
            cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            
            cursor.execute(query_psycopg2, params_tuple)
            
            if "RETURNING" in sql.upper():
                result = cursor.fetchall()
                conn.commit()
                return [dict(row) for row in result]
            else:
                conn.commit()
                return []

        finally:
            if conn:
                conn.close()