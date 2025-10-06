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
    SORT_KEY = "organization"
    TABLE_NAME = "warnings"
    
    @staticmethod
    def partition_key_format(warning_id: str) -> str:
        return f"warning#{warning_id}"
    
    @staticmethod
    def sort_key_format(organization: str) -> str:
        return f"organization#{organization}"

    def __init__(self):
        envs = Environments.get_envs()
        
        self.dynamo = DynamoDatasource(endpoint_url=f'{envs.DYNAMO_ENDPOINT_URL}:{envs.DYNAMO_ENDPOINT_PORT}',
                                       dynamo_table_name=self.TABLE_NAME,
                                       region=envs.DYNAMO_REGION,
                                       partition_key=self.PARTITION_KEY,
                                       sort_key=self.SORT_KEY)
        
    def create_warning(self, new_warning: Warning, target_org: ORGANIZATION, target_role: ROLE) -> Optional[Warning]:
        item = {};
        item['warning_id'] = self.partition_key_format(new_warning.warning_id)
        item['organization'] = self.sort_key_format(target_org.value)
        # Para evitar problemas com a conversão para JSON, convertendo datetime para isoformat
        item['body'] = json.dumps(new_warning.model_dump() | {"expire": new_warning.expire.isoformat()})
        item['target_role'] = target_role.value
        
        self.dynamo.put_item(item=item, partition_key=item['warning_id'], sort_key=item['organization'])
        
        return new_warning

    def get_warning(self, warning_id: str, target_org: ORGANIZATION) -> Optional[Warning]:
        try:
            item: dict = self.dynamo.get_item(partition_key=self.partition_key_format(warning_id), sort_key=self.sort_key_format(target_org.value))
            body = json.loads(item['Item']['body'])
            return Warning(**body)
        except Exception as e:
            raise Exception(f'Warning with id {warning_id} not found.')
    
    def update_warning(self, warning_id: str, organization: ORGANIZATION, warning: Warning) -> Optional[Warning]:
        self.get_warning(warning_id, organization)  # Check if exists before updating
        
        item = {}
        item['body'] = json.dumps(warning.model_dump() | {"expire": warning.expire.isoformat()})
        self.dynamo.update_item(partition_key=self.partition_key_format(warning_id), sort_key=self.sort_key_format(organization.value), update_dict=item)
        return warning

    def delete_warning(self, warning_id: str, organization: ORGANIZATION) -> Optional[Warning]:
        existing_warning = self.get_warning(warning_id, organization)
        self.dynamo.delete_item(partition_key=self.partition_key_format(warning_id), sort_key=self.sort_key_format(organization.value))
        return existing_warning  # Return the deleted warning

    def get_all_warnings(self):
        items = self.dynamo.get_all_items()
        warnings = []
        for item in items.get('Items', []):
            body = json.loads(item['body'])
            warnings.append(Warning(**body))
        return warnings