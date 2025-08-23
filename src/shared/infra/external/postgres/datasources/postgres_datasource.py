import os
import boto3
from typing import Any, Dict, List, Optional, Sequence, Tuple, Union

class RdsDataDatasource:
    """
    Simple wrapper to use AWS RDS Data API (Aurora Serverless + Data API)
    Requires envs: DB_CLUSTER_ARN, DB_SECRET_ARN, DB_NAME
    """
    def __init__(
        self,
        cluster_arn: Optional[str] = None,
        secret_arn: Optional[str]  = None,
        database: Optional[str]    = None,
        region_name: Optional[str] = None,
    ):
        self.cluster_arn = cluster_arn or os.environ["DB_CLUSTER_ARN"]
        self.secret_arn  = secret_arn  or os.environ["DB_SECRET_ARN"]
        self.database    = database    or os.environ.get("DB_NAME")
        self.client = boto3.client("rds-data", region_name=region_name)

    @staticmethod
    def _to_sql_params(params: Optional[Union[Tuple, List, Dict[str, Any]]]):
        if not params:
            return None
        def _one(val):
            if val is None: return {"isNull": True}
            if isinstance(val, bool): return {"booleanValue": val}
            if isinstance(val, int): return {"longValue": val}
            if isinstance(val, float): return {"doubleValue": val}
            return {"stringValue": str(val)}
        if isinstance(params, dict):
            return [{"name": k, "value": _one(v)} for k, v in params.items()]
        if isinstance(params, (list, tuple)):
            return [{"value": _one(v)} for v in params]
        raise TypeError("Params must be dict or sequence")
    
    @staticmethod
    def _records_to_dicts(column_metadata, records) -> List[Dict[str, Any]]:
        cols = [c.get("name") for c in (column_metadata or [])]
        out: List[Dict[str, Any]] = []
        for r in records or []:
            row: Dict[str, Any] = {}
            for i, field in enumerate(r):
                val = None
                for k, v in field.items():
                    if k.endswith("Value"):
                        val = v
                        break
                key = cols[i] if i < len(cols) else f"col_{i}"
                row[key] = val
            out.append(row)
        return out

    # def execute(
    #     self,
    #     query: str,
    #     params: Optional[Union[Tuple, List, Dict[str, Any]]] = None,
    #     transaction_id: Optional[str] = None,
    #     include_result: bool = True,
    # ) -> List[Dict[str, Any]]:
    #     kwargs = dict(
    #         resourceArn=self.cluster_arn,
    #         secretArn=self.secret_arn,
    #         sql=query,
    #         database=self.database,
    #     )
    #     sql_params = self._to_sql_params(params)
    #     if sql_params: kwargs["parameters"] = sql_params
    #     if transaction_id: kwargs["transactionId"] = transaction_id
    #     resp = self.client.execute_statement(**kwargs)
    #     if not include_result: return []
    #     return self._records_to_dicts(resp.get("columnMetadata"), resp.get("records"))

    # def begin(self) -> str:
    #     resp = self.client.begin_transaction(
    #         resourceArn=self.cluster_arn,
    #         secretArn=self.secret_arn,
    #         database=self.database,
    #     )
    #     return resp["transactionId"]

    # def commit(self, transaction_id: str):
    #     self.client.commit_transaction(
    #         resourceArn=self.cluster_arn,
    #         secretArn=self.secret_arn,
    #         transactionId=transaction_id,
    #     )

    # def rollback(self, transaction_id: str):
    #     self.client.rollback_transaction(
    #         resourceArn=self.cluster_arn,
    #         secretArn=self.secret_arn,
    #         transactionId=transaction_id,
    #     )
