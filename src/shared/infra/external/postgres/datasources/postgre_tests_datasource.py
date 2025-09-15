import psycopg2
import psycopg2.extras
from typing import Optional, Dict, Any, List
import re

class PostgresTestDatasource:
    """
    Datasource para testes de integração que se conecta a um banco PostgreSQL local.
    """
    def __init__(self):
        self.connection_params = {
            "dbname": "mydatabase",
            "user": "myuser",
            "password": "mypassword",
            "host": "localhost",
            "port": "5432"
        }
        self.conn = psycopg2.connect(**self.connection_params)
        
    def _translate_query(self, sql, params):
        """ 
        Traduz a query de :key para %(key)s e garante que os parâmetros
        estejam na ordem correta para execução.
        Necessário pois o psycopg2 fala uma língua diferente do rds aurora!
        """
        # Usa uma expressão regular para encontrar todos os :placeholders
        param_keys = re.findall(r':(\w+)', sql)
        
        # Substitui cada :placeholder por %s
        query_psycopg2 = re.sub(r':(\w+)', '%s', sql)
        
        # Cria uma tupla de valores na ordem exata em que aparecem na query
        params_tuple = tuple(params[key] for key in param_keys)
        
        return query_psycopg2, params_tuple

    def query(self, sql: str, params: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """
        Executa uma query e retorna os resultados como uma lista de dicionários.
        """
        query_psycopg2, params_tuple = self._translate_query(sql, params)
       
        with self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
            cursor.execute(query_psycopg2, params_tuple)
            
            results = []
            if "RETURNING" in sql.upper() or sql.upper().strip().startswith("SELECT"):
                results = [dict(row) for row in cursor.fetchall()]
            
            self.conn.commit()
            return results

    def execute(self, sql: str, params: Optional[Dict[str, Any]] = None) -> int:
        """
        Executa um comando e retorna o número de linhas afetadas.
        """
        
        query_psycopg2, params_tuple = self._translate_query(sql, params)
        
        with self.conn.cursor() as cursor:
            cursor.execute(query_psycopg2, params_tuple)
            rowcount = cursor.rowcount
            self.conn.commit()
            return rowcount

    def close(self):
        """Fecha a conexão com o banco de dados."""
        if self.conn:
            self.conn.close()

    def __del__(self):
        self.close()