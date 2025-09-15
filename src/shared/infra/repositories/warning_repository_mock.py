from src.shared.domain.entities.warning import Warning
from src.shared.domain.repositories.warning_repository_interface import IWarningRepository
import datetime
from dataclasses import dataclass
from src.shared.domain.enums.role_enum import ROLE
from typing import *
from src.shared.helpers.errors.usecase_errors import NoItemsFound

@dataclass
class UserWarningLink:
    user_id: str
    warning_id: str
    
@dataclass
class RoleWarningLink:
    role: ROLE
    warning_id: str

class WarningRepositoryMock(IWarningRepository):
    
    def __init__(self):
        
        #tabela de avisos
        #armazena as entidades avisos com usas respectivas informações
        
        self.warnings = [
            Warning(
                title="Titulo do alerta 1",
                description="Descrição do alerta 1",
                expire=datetime.datetime.now(datetime.UTC),
                viewed=False,
                warning_id="e6112d17-c030-4d65-8b9f-e472d20055a5"
            ),
            Warning(
                title="Titulo do alerta 2",
                description="Descrição do alerta 2",
                expire=datetime.datetime.now(datetime.UTC),
                viewed=True,
                warning_id="0f9806f9-1baf-4df4-95ac-61011e190189"
            )
        ]
        
        #tabela de avisos-role, usada para uma relação direta entre roles e warning_ids
        #facilita a busca em grupos
        #a tabela esta aqui pois retorna warnings
        #isso apeans simula uma tabela, a dataclass é irrelevante
        
        self.user_warning = [
            UserWarningLink(
                user_id="550e8400-e29b-41d4-a716-446655440002", 
                warning_id="e6112d17-c030-4d65-8b9f-e472d20055a5"
            ),
            UserWarningLink(
                user_id="e6bed58f-424a-4b62-b408-18e0a8d1f069",
                warning_id="0f9806f9-1baf-4df4-95ac-61011e190189"
            )
        ]
        
        #tabela de avisos-usuários, usada para uma relação direta entre user_id e warning_id
        #facilita imensamente a busca individual
        #essa tabela esta no banco de avisos pois os getters retornam avisos e nao usuarios
        #isso apeans simula uma tabela, a dataclass é irrelevante
        
        self.role_warning = [
            RoleWarningLink(
                role=ROLE.PRESIDENT,
                warning_id="e6112d17-c030-4d65-8b9f-e472d20055a5"
            ),
            RoleWarningLink(
                role=ROLE.PRESIDENT,
                warning_id="0f9806f9-1baf-4df4-95ac-61011e190189"
            )
        ]
        
    def create_warning(self, new_warning: Warning) -> Optional[Warning]:
                        
        self.warnings.append(new_warning)
        
        return new_warning
    
    def link_to_users(self, warning_id: str, user_ids: list[str]) -> None:
        
        for user_id in user_ids:
            
            self.user_warning.append(UserWarningLink(warning_id=warning_id, user_id=user_id))
            
    def link_to_roles(self, warning_id: str, roles: list[ROLE]):
        
        for role in roles:
            
            self.role_warning.append(RoleWarningLink(warning_id=warning_id, role=role))
    
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
        
        #o alerta precisa ser deletado das outras tabelas    
        
        for i, existing_user_alert_link in enumerate(self.user_warning):
            
            if existing_user_alert_link.warning_id == warning_id:
                
                self.user_warning.pop(i)

                break
            
        for i, existing_role_alert_link in enumerate(self.role_warning):
            
            if existing_role_alert_link.warning_id == warning_id:
                
                self.role_warning.pop(i)
                                
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
    
    def get_user_warnings(self, user_id: str) -> Optional[Warning]:
        
        target_warning_ids = [
            link.warning_id 
            for link in self.user_warning 
            if link.user_id == user_id
        ]
        
        warnings_found = []
        
        for warning_id in target_warning_ids:
            
            warning = self.get_warning(warning_id)
            
            if warning:
                
                warnings_found.append(warning)
                
        return warnings_found
    
    def get_president_warnings(self) -> Optional[Warning]:
        
        target_warning_ids = [
            link.warning_id
            for link in self.role_warning
            if link.role == ROLE.PRESIDENT
        ]
        
        warnings_found = []
        
        for warning_id in target_warning_ids:
            
            warning = self.get_warning(warning_id)
                
            if warning:
                
                warnings_found.append(warning)
                
        return warnings_found