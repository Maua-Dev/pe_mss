import os
import boto3
import logging
from contextlib import contextmanager
from datetime import datetime
from typing import Any, Dict, List, Optional, Generator

# Configuração básica de logging para o módulo
logger = logging.getLogger(__name__)

class RdsDataError(Exception):
    """Exceção personalizada para erros originados no RdsDataDatasource."""
    pass

class RdsDataDatasource:
    """
    Um wrapper robusto para a AWS RDS Data API, projetado para interações
    com bancos de dados como o Aurora Serverless (PostgreSQL/MySQL).

    Esta classe abstrai a complexidade da API, oferecendo uma interface
    simples e segura para executar queries, operações em lote e gerenciar
    transações.

    Requer as seguintes variáveis de ambiente para configuração padrão:
    - DB_CLUSTER_ARN: O ARN do cluster do Aurora Serverless.
    - DB_SECRET_ARN: O ARN do segredo no AWS Secrets Manager.
    - DB_NAME: O nome do banco de dados a ser utilizado.
    """

    def __init__(
        self,
        cluster_arn: Optional[str] = None,
        secret_arn: Optional[str] = None,
        database: Optional[str] = None,
        region_name: Optional[str] = None,
    ):
        """
        Inicializa o datasource e o cliente boto3 para o RDS Data API.

        Args:
            cluster_arn (Optional[str]): O ARN do cluster RDS. Se não for fornecido,
                                         busca da variável de ambiente 'DB_CLUSTER_ARN'.
            secret_arn (Optional[str]): O ARN do segredo do Secrets Manager. Se não
                                        for fornecido, busca de 'DB_SECRET_ARN'.
            database (Optional[str]): O nome do banco de dados. Se não for fornecido,
                                      busca de 'DB_NAME'.
            region_name (Optional[str]): A região da AWS. Se não fornecida, usa a
                                         configuração padrão do boto3.
        """
        self.cluster_arn = cluster_arn or os.environ["DB_CLUSTER_ARN"]
        self.secret_arn = secret_arn or os.environ["DB_SECRET_ARN"]
        self.database = database or os.environ.get("DB_NAME")
        self.client = boto3.client("rds-data", region_name=region_name)
        logger.info(f"RdsDataDatasource inicializado para o banco '{self.database}'.")

    @staticmethod
    def _to_sql_params(params: Optional[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        [Interno] Converte um dicionário Python para o formato de parâmetros da RDS Data API.

        Args:
            params (Optional[Dict[str, Any]]): Dicionário de parâmetros nomeados.

        Returns:
            List[Dict[str, Any]]: Lista de parâmetros formatada para a API.
        
        Raises:
            TypeError: Se um tipo de valor não for suportado.
        """
        if not params:
            return []

        sql_params = []
        for k, v in params.items():
            if v is None:
                value = {"isNull": True}
            elif isinstance(v, bool):
                value = {"booleanValue": v}
            elif isinstance(v, str):
                value = {"stringValue": v}
            elif isinstance(v, int):
                value = {"longValue": v}
            elif isinstance(v, float):
                value = {"doubleValue": v}
            elif isinstance(v, datetime):
                value = {"stringValue": v.strftime('%Y-%m-%d %H:%M:%S.%f')}
            # Adicione aqui outros tipos como 'blobValue' se necessário
            else:
                raise TypeError(f"Tipo de parâmetro não suportado para '{k}': {type(v)}")
            
            sql_params.append({"name": k, "value": value})
        return sql_params

    @staticmethod
    def _records_to_dicts(column_metadata: List[Dict], records: List[List[Dict]]) -> List[Dict[str, Any]]:
        """
        [Interno] Converte a resposta de 'records' da API em uma lista de dicionários Python.

        Args:
            column_metadata (List[Dict]): Metadados das colunas da resposta.
            records (List[List[Dict]]): Registros retornados pela API.

        Returns:
            List[Dict[str, Any]]: Uma lista de dicionários, onde cada um representa uma linha.
        """
        if not column_metadata or not records:
            return []
            
        columns = [c["name"] for c in column_metadata]
        result = []
        for record in records:
            row = {}
            for i, field in enumerate(record):
                # Extrai o valor do primeiro (e único) campo dentro do 'field' dict
                # Ex: de {'stringValue': 'valor'} para 'valor'
                value = next(iter(field.values()), None)
                row[columns[i]] = value
            result.append(row)
        return result

    def query(
        self,
        sql: str,
        params: Optional[Dict[str, Any]] = None,
        transaction_id: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        Executa uma consulta SQL de leitura (ex: SELECT) e retorna os resultados.

        Args:
            sql (str): A string da consulta SQL a ser executada.
            params (Optional[Dict[str, Any]]): Dicionário de parâmetros para a consulta.
            transaction_id (Optional[str]): ID de uma transação existente, se aplicável.

        Returns:
            List[Dict[str, Any]]: Uma lista de dicionários representando as linhas retornadas.
        
        Raises:
            RdsDataError: Em caso de falha na execução da consulta.
        """
        kwargs = {
            "resourceArn": self.cluster_arn,
            "secretArn": self.secret_arn,
            "database": self.database,
            "sql": sql,
            "parameters": self._to_sql_params(params),
            "includeResultMetadata": True,
        }
        if transaction_id:
            kwargs["transactionId"] = transaction_id
        
        try:
            logger.debug(f"Executando query: {sql} com params: {params}")
            response = self.client.execute_statement(**kwargs)
            return self._records_to_dicts(
                response.get("columnMetadata", []), response.get("records", [])
            )
        except self.client.exceptions.ClientError as e:
            logger.error(f"Erro ao executar query: {e.response['Error']['Message']}")
            raise RdsDataError(e) from e

    def execute(
        self,
        sql: str,
        params: Optional[Dict[str, Any]] = None,
        transaction_id: Optional[str] = None,
    ) -> int:
        """
        Executa uma instrução SQL de escrita (INSERT, UPDATE, DELETE) e retorna o número
        de linhas afetadas.

        Args:
            sql (str): A instrução SQL a ser executada.
            params (Optional[Dict[str, Any]]): Dicionário de parâmetros para a instrução.
            transaction_id (Optional[str]): ID de uma transação existente, se aplicável.

        Returns:
            int: O número de registros afetados pela instrução.
            
        Raises:
            RdsDataError: Em caso de falha na execução.
        """
        kwargs = {
            "resourceArn": self.cluster_arn,
            "secretArn": self.secret_arn,
            "database": self.database,
            "sql": sql,
            "parameters": self._to_sql_params(params),
        }
        if transaction_id:
            kwargs["transactionId"] = transaction_id
            
        try:
            logger.debug(f"Executando statement: {sql} com params: {params}")
            response = self.client.execute_statement(**kwargs)
            return response.get("numberOfRecordsUpdated", 0)
        except self.client.exceptions.ClientError as e:
            logger.error(f"Erro ao executar statement: {e.response['Error']['Message']}")
            raise RdsDataError(e) from e

    def batch_execute(
        self,
        sql: str,
        params_list: List[Dict[str, Any]],
        transaction_id: Optional[str] = None,
    ) -> int:
        """
        Executa uma instrução SQL em lote com múltiplos conjuntos de parâmetros.
        Ideal para inserções ou atualizações em massa.

        Args:
            sql (str): A instrução SQL a ser executada.
            params_list (List[Dict[str, Any]]): Uma lista de dicionários de parâmetros.
            transaction_id (Optional[str]): O ID da transação, se aplicável.

        Returns:
            int: O número total de registros afetados.
            
        Raises:
            RdsDataError: Em caso de falha na execução.
        """
        if not params_list:
            return 0

        kwargs = {
            "resourceArn": self.cluster_arn,
            "secretArn": self.secret_arn,
            "database": self.database,
            "sql": sql,
            "parameterSets": [self._to_sql_params(p) for p in params_list],
        }
        if transaction_id:
            kwargs["transactionId"] = transaction_id

        try:
            logger.info(f"Executando batch para {len(params_list)} registros.")
            self.client.batch_execute_statement(**kwargs)
            return len(params_list)
        except self.client.exceptions.ClientError as e:
            logger.error(f"Erro ao executar batch statement: {e.response['Error']['Message']}")
            raise RdsDataError(e) from e

    @contextmanager
    def transaction(self) -> Generator[str, None, None]:
        """
        Fornece um contexto de transação que gerencia automaticamente o commit e o rollback.
        Use com a instrução 'with'.

        Yields:
            str: O ID da transação para ser usado nas chamadas de 'query' e 'execute'.

        Example:
            with db.transaction() as tx_id:
                db.execute(sql1, params1, transaction_id=tx_id)
                db.execute(sql2, params2, transaction_id=tx_id)
        """
        transaction_id = ""
        try:
            response = self.client.begin_transaction(
                resourceArn=self.cluster_arn,
                secretArn=self.secret_arn,
                database=self.database,
            )
            transaction_id = response["transactionId"]
            logger.info(f"Transação iniciada: {transaction_id}")
            yield transaction_id
            
            # Se o bloco 'with' terminar sem exceções, commita.
            self.client.commit_transaction(
                resourceArn=self.cluster_arn,
                secretArn=self.secret_arn,
                transactionId=transaction_id,
            )
            logger.info(f"Transação commitada: {transaction_id}")
            
        except Exception as e:
            logger.error(f"Erro durante a transação {transaction_id}, iniciando rollback.")
            if transaction_id:
                try:
                    self.client.rollback_transaction(
                        resourceArn=self.cluster_arn,
                        secretArn=self.secret_arn,
                        transactionId=transaction_id,
                    )
                    logger.warning(f"Transação revertida (rollback): {transaction_id}")
                except self.client.exceptions.ClientError as rollback_error:
                    # Loga o erro de rollback, mas relança a exceção original
                    logger.critical(f"Falha ao reverter transação {transaction_id}: {rollback_error}")
            # Relança a exceção original que causou o rollback
            raise RdsDataError(f"Transaction failed and was rolled back: {e}") from e