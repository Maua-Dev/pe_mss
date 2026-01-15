from src.shared.domain.entities.warning import Warning, WarningBody
from src.shared.domain.enums.organization_enum import ORGANIZATION
from src.shared.domain.repositories.warning_repository_interface import IWarningRepository
import datetime
from dataclasses import dataclass
from src.shared.domain.enums.role_enum import ROLE
from typing import *
from src.shared.helpers.errors.usecase_errors import NoItemsFound

class WarningRepositoryMock(IWarningRepository):
    
    def __init__(self):
        
        #tabela de avisos
        #armazena as entidades avisos com usas respectivas informações
        
        self.warnings = [
            Warning(
                warning_id="e6112d17-c030-4d65-8b9f-e472d20055a5",
                target_role=ROLE.PRESIDENT,
                target_org=ORGANIZATION.DEV,
                body=WarningBody(
                    title="Titulo do alerta 1",
                    description="Descrição do alerta 1",
                    expire=int((datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=10)).timestamp() * 1000)
                ),
                created_at=int((datetime.datetime.now(datetime.timezone.utc)).timestamp() * 1000)
            ),
            Warning(
                warning_id="0f9806f9-1baf-4df4-95ac-61011e190189",
                target_role=ROLE.PRESIDENT,
                target_org=ORGANIZATION.NAWAT,
                body=WarningBody(
                    title="Titulo do alerta 2",
                    description="Descrição do alerta 2",
                    expire=int((datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=5)).timestamp() * 1000)
                ),
                created_at=int((datetime.datetime.now(datetime.timezone.utc)).timestamp() * 1000)
            ),
            Warning(
                warning_id="1f9806f9-1baf-4df4-95ac-61011e190189",
                target_role=ROLE.PRESIDENT,
                target_org=ORGANIZATION.ESPORTS,
                body=WarningBody(
                    title="Titulo do alerta 3",
                    description="Descrição do alerta 3",
                    expire=int((datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=2)).timestamp() * 1000)
                ),
                created_at=int((datetime.datetime.now(datetime.timezone.utc)).timestamp() * 1000)
            ),
            Warning(
                warning_id="2f9806f9-1baf-4df4-95ac-61011e190189",
                target_role=ROLE.PRESIDENT,
                target_org=ORGANIZATION.NAWAT,
                body=WarningBody(
                    title="Titulo do alerta 4",
                    description="Descrição do alerta 4",
                    expire=int((datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=7)).timestamp() * 1000)
                ),
                created_at=int((datetime.datetime.now(datetime.timezone.utc)).timestamp() * 1000)
            )
        ]
        
    def create_warning(self, new_warning: Warning) -> Optional[Warning]:
                        
        self.warnings.append(new_warning)
        
        return new_warning
    
    def update_warning(self, warning: Warning) -> Optional[Warning]:
        
        warning_found = False
        
        for i, existing_warning in enumerate(self.warnings):
            
            if existing_warning.warning_id == warning.warning_id:
                
                self.warnings[i] = warning
                
                warning_found = True
                
                break
        
        if not warning_found:
            
            raise NoItemsFound(warning.warning_id)
        
        return warning
    
    def delete_warning(self, warning_id: str) -> Optional[Warning]:
        
        #simplificando uma transaction em SQL pro mock
        #simples validacao se o alerta foi encontado na tabela principal
        
        warning_found = False
                
        for i, existing_warning in enumerate(self.warnings):
            
            if existing_warning.warning_id == warning_id:
                
                deleted_warning = self.warnings.pop(i)
                
                warning_found = True
                
                break
            
        if not warning_found:
            
            raise NoItemsFound(warning_id)
        
        return deleted_warning
    
    def get_warning(self, warning_id: str) -> Optional[Warning]:
        
        for existing_warning in self.warnings:
            
            if existing_warning.warning_id == warning_id:
                
                return existing_warning
            
        raise NoItemsFound(warning_id)
    
    def get_all_warnings(self):
        
        return self.warnings
    
    def get_warnings_by_org(self, target_org: ORGANIZATION) -> List[Warning]:        
        org_warnings = [warning for warning in self.warnings if ORGANIZATION(warning.target_org) == target_org]
        
        if not org_warnings:
            raise NoItemsFound(f"No warnings found for organization: {target_org}")

        return org_warnings
    
    def get_warnings_by_role(self, target_role: ROLE) -> List[Warning]:
        
        role_warnings = [warning for warning in self.warnings if ROLE(warning.target_role) == target_role]
        
        if not role_warnings:
            raise NoItemsFound(f"No warnings found for role: {target_role}")
        
        return role_warnings
    
    def get_warnings_by_org_and_role(self, target_org: ORGANIZATION, target_role: ROLE) -> List[Warning]:
        
        org_role_warnings = [warning for warning in self.warnings if ORGANIZATION(warning.target_org) == target_org and ROLE(warning.target_role) == target_role]
        
        if not org_role_warnings:
            raise NoItemsFound(f"No warnings found for organization: {target_org} and role: {target_role}")
        
        return org_role_warnings