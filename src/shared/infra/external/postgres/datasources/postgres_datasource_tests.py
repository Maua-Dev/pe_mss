import psycopg2
import psycopg2.extras
from typing import Optional, Dict, Any, List, Generator
import re
from contextlib import contextmanager
import logging

logger = logging.getLogger(__name__)

class TestsRdsDatasource:
    """
    Datasource para testes de integração que mimetiza o comportamento da
    RdsDataDatasource, conectando-se a um banco PostgreSQL local.
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
        self._in_transaction = False

    @staticmethod
    def _translate_query(sql: str) -> str:
        """ 
        Traduz a query do formato :key para o formato %(key)s, que o psycopg2
        entende para parâmetros nomeados.
        """
        return re.sub(r':(\w+)', r'%(\1)s', sql)

    def query(
        self, 
        sql: str, 
        params: Optional[Dict[str, Any]] = None, 
        transaction_id: Optional[str] = None 
    ) -> List[Dict[str, Any]]:
        """
        Executa uma query e retorna os resultados. O commit só é realizado
        se não estiver dentro de um bloco de transação explícito.
        """
        if params is None:
            params = {}
        
        query_psycopg2 = self._translate_query(sql)
        
        try:
            with self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
                cursor.execute(query_psycopg2, params)
                
                results = []
                if cursor.description:
                    results = [dict(row) for row in cursor.fetchall()]
                
                if not self._in_transaction:
                    self.conn.commit()
                
                return results
        except Exception as e:
            if not self._in_transaction:
                self.conn.rollback()
            logger.error(f"Erro ao executar query de teste: {e}")
            raise

    def execute(
        self, 
        sql: str, 
        params: Optional[Dict[str, Any]] = None,
        transaction_id: Optional[str] = None
    ) -> int:
        """
        Executa um comando (INSERT, UPDATE, DELETE) e retorna o número de linhas afetadas.
        """
        if params is None:
            params = {}

        query_psycopg2 = self._translate_query(sql)
        
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(query_psycopg2, params)
                rowcount = cursor.rowcount
                
                if not self._in_transaction:
                    self.conn.commit()
                    
                return rowcount
        except Exception as e:
            if not self._in_transaction:
                self.conn.rollback()
            logger.error(f"Erro ao executar statement de teste: {e}")
            raise

    def batch_execute(
        self, 
        sql: str, 
        params_list: List[Dict[str, Any]], 
        transaction_id: Optional[str] = None
    ) -> int:
        """
        Executa um comando em lote.
        """
        if not params_list:
            return 0
        
        query_psycopg2 = self._translate_query(sql)
        
        try:
            with self.conn.cursor() as cursor:
                psycopg2.extras.execute_batch(cursor, query_psycopg2, params_list)
                rowcount = cursor.rowcount

                if not self._in_transaction:
                    self.conn.commit()

                return rowcount
        except Exception as e:
            if not self._in_transaction:
                self.conn.rollback()
            logger.error(f"Erro ao executar batch de teste: {e}")
            raise

    @contextmanager
    def transaction(self) -> Generator[str, None, None]:
        """
        Fornece um contexto de transação que mimetiza a RdsDataDatasource.
        Gerencia o estado da transação, o commit e o rollback.
        """
        if self._in_transaction:
            raise Exception("Transações aninhadas não são suportadas neste mock.")

        self._in_transaction = True
        logger.debug("Transação de teste iniciada.")
        try:
            yield "mock_transaction_id"
            self.conn.commit()
            logger.debug("Transação de teste commitada.")
        except Exception as e:
            self.conn.rollback()
            logger.error(f"Transação de teste revertida (rollback) devido a erro: {e}")
            raise e
        finally:
            self._in_transaction = False

    def close(self):
        """Fecha a conexão com o banco de dados."""
        if self.conn and not self.conn.closed:
            self.conn.close()
            logger.info("Conexão de teste com o banco de dados fechada.")

    def __del__(self):
        self.close()