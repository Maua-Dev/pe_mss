import json
from typing import Optional

from pydantic_core import from_json
from src.shared.domain.enums.organization_enum import ORGANIZATION
from src.shared.domain.entities.warning import Warning
from src.shared.domain.enums.role_enum import ROLE
from src.shared.domain.repositories.warning_repository_interface import IWarningRepository
from src.shared.environments import Environments
from src.shared.infra.external.dynamo.datasources.dynamo_datasource import DynamoDatasource


class WarningRepositoryDynamo(IWarningRepository):
    PARTITION_KEY = "warning_id"
    TABLE_NAME = Environments.get_envs().warning_table_name
    
    @staticmethod
    def partition_key_format(warning_id: str) -> str:
        return f"warning#{warning_id}"
    
    @staticmethod
    def remove_prefixo(parametro: str):
        
        partes = parametro.split('#', 1) 
        
        if len(partes) > 1:
            parametro = partes[1]
            
        return parametro
    
    # @staticmethod
    # def sort_key_format(target_org: str) -> str:
    #     return f"target_org#{target_org}"

    def __init__(self):
        envs = Environments.get_envs()

        self.dynamo = DynamoDatasource(
            endpoint_url=envs.endpoint_url,
            dynamo_table_name=self.TABLE_NAME,
            region=envs.dynamo_region,
            partition_key=self.PARTITION_KEY,
        )
        
    def create_warning(self, new_warning: Warning) -> Optional[Warning]:
        item = new_warning.model_dump_json()
        item = json.loads(item)
        item['warning_id'] = self.partition_key_format(new_warning.warning_id)
        # item['target_org'] = self.sort_key_format(new_warning.target_org)

        self.dynamo.put_item(item=item, partition_key=item['warning_id'])
        
        return new_warning

    def get_warning(self, warning_id: str) -> Optional[Warning]:
        try:
            item = self.dynamo.get_item(partition_key=self.partition_key_format(warning_id))
            # item['Item']['target_org'] = item['Item']['target_org'].split('#')[1]
            item["Item"]["warning_id"] = self.remove_prefixo(item["Item"]["warning_id"])
            warning = Warning.model_validate(item['Item'])
            return warning
        except Exception as e:
            raise Exception(f'Warning with id {warning_id} not found.')
    
    def update_warning(self, warning_id: str, warning: Warning) -> Optional[Warning]:
        self.get_warning(warning_id)
        
        item = {}
        item['body'] = json.loads(warning.body.model_dump_json())

        self.dynamo.update_item(partition_key=self.partition_key_format(warning_id), update_dict=item)
        return warning

    def delete_warning(self, warning_id: str) -> Optional[Warning]:
        existing_warning = self.get_warning(warning_id)
        self.dynamo.delete_item(partition_key=self.partition_key_format(warning_id))
        return existing_warning  # Return the deleted warning

    def get_all_warnings(self):
        items = self.dynamo.get_all_items()['Items']
        warnings = []
        
        for item in items:
            
            item["warning_id"] = self.remove_prefixo(item["warning_id"])
            warning = Warning.model_validate(item)
            warnings.append(warning)
            
        return warnings
    
    def get_warnings_by_org(self, target_org: ORGANIZATION) -> list[Warning]:
        response = self.dynamo.query(
            TableName='warnings',
            IndexName='OrganizationIndex',
            KeyConditionExpression='target_org = :org',
            ExpressionAttributeValues={
                ':org': target_org.value
            }
        )
        
        warnings = []
        
        for warning_json in response["Items"]:
            
            warning_json["warning_id"] = self.remove_prefixo(warning_json["warning_id"])
            warnings.append(Warning.model_validate(warning_json))
            
        return warnings
    
    def get_warnings_by_role(self, target_role: ROLE) -> list[Warning]:
        response = self.dynamo.query(
            TableName='warnings',
            IndexName='RoleIndex',
            KeyConditionExpression='target_role = :role',
            ExpressionAttributeValues={
                ':role': target_role.value
            }
        )
        
        warnings = []
        
        for warning_json in response["Items"]:
            
            warning_json["warning_id"] = self.remove_prefixo(warning_json["warning_id"])
            warnings.append(Warning.model_validate(warning_json))
            
        return warnings
    
    # NOT WORKING - NEEDS NEW GSI WITH BOTH target_org AND target_role AS KEYS 
    # NOT NEEDED FOR NOW
    def get_warnings_by_org_and_role(self, target_org: ORGANIZATION, target_role: ROLE) -> list[Warning]:
        pass
    # def get_warnings_by_org_and_role(self, target_org: ORGANIZATION, target_role: ROLE) -> list[Warning]:
    #     response = self.dynamo.query(
    #         TableName='warnings',
    #         IndexName='RoleIndex',
    #         KeyConditionExpression='target_org = :org AND target_role = :role',
    #         ExpressionAttributeValues={
    #             ':org': target_org.value,
    #             ':role': target_role.value
    #         }
    #     )
        
    #     warnings = []
        
    #     for warning_json in response["Items"]:
            
    #         warning_json["warning_id"] = self.remove_prefixo(warning_json["warning_id"])
    #         warnings.append(Warning.model_validate(warning_json))
            
    #     return warnings