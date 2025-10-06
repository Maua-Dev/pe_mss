import json
from typing import Optional
from src.shared.domain.enums.organization_enum import ORGANIZATION
from src.shared.domain.entities.warning import Warning
from src.shared.domain.enums.role_enum import ROLE
from src.shared.domain.repositories.warning_repository_interface import IWarningRepository
from src.shared.environments import Environments
from src.shared.infra.external.dynamo.datasources.dynamo_datasource import DynamoDatasource


class WarningRepositoryDynamo(IWarningRepository):
    PARTITION_KEY = "warning_id"
    TABLE_NAME = "warnings"
    
    @staticmethod
    def partition_key_format(warning_id: str) -> str:
        return f"warning#{warning_id}"
    
    @staticmethod
    def sort_key_format(target_org: str) -> str:
        return f"target_org#{target_org}"

    def __init__(self):
        envs = Environments.get_envs()

        self.dynamo = DynamoDatasource(endpoint_url=f'{envs.dynamo_endpoint_url}:{envs.dynamo_endpoint_port}',
                                       dynamo_table_name=self.TABLE_NAME,
                                       region=envs.dynamo_region,
                                       partition_key=self.PARTITION_KEY,
                                       )
        
    def create_warning(self, new_warning: Warning, target_org: ORGANIZATION, target_role: ROLE) -> Optional[Warning]:
        item = {};
        item['warning_id'] = self.partition_key_format(new_warning.warning_id)
        item['target_org'] = self.sort_key_format(target_org.value)
        # Para evitar problemas com a conversão para JSON, convertendo datetime para isoformat
        item['body'] = json.dumps(new_warning.model_dump() | {"expire": new_warning.expire.isoformat()})
        item['target_role'] = target_role.value

        self.dynamo.put_item(item=item, partition_key=item['warning_id'])
        
        return new_warning

    def get_warning(self, warning_id: str) -> Optional[Warning]:
        try:
            item: dict = self.dynamo.get_item(partition_key=self.partition_key_format(warning_id))
            body = json.loads(item['Item']['body'])
            return Warning(**body)
        except Exception as e:
            raise Exception(f'Warning with id {warning_id} not found.')
    
    def update_warning(self, warning_id: str, warning: Warning) -> Optional[Warning]:
        self.get_warning(warning_id)  # Check if exists before updating
        
        item = {}
        item['body'] = json.dumps(warning.model_dump() | {"expire": warning.expire.isoformat()})
        self.dynamo.update_item(partition_key=self.partition_key_format(warning_id), update_dict=item)
        return warning

    def delete_warning(self, warning_id: str) -> Optional[Warning]:
        existing_warning = self.get_warning(warning_id)
        self.dynamo.delete_item(partition_key=self.partition_key_format(warning_id))
        return existing_warning  # Return the deleted warning

    def get_all_warnings(self):
        items = self.dynamo.get_all_items()
        warnings = []
        for item in items.get('Items', []):
            body = json.loads(item['body'])
            warnings.append(Warning(**body))
        return warnings