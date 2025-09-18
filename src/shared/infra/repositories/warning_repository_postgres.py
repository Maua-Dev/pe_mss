from src.shared.domain.entities.warning import Warning
from src.shared.domain.repositories.warning_repository_interface import IWarningRepository
from src.shared.infra.external.postgres.datasources.postgres_datasource import RdsDataDatasource
from src.shared.infra.external.postgres.datasources.postgres_datasource_tests import TestsRdsDatasource
from src.shared.domain.enums.role_enum import ROLE
from typing import *

class WarningRepositoryPostgres(IWarningRepository):
    def __init__(self, db_datasource: Union[RdsDataDatasource, TestsRdsDatasource]):
        self.postgres = db_datasource
        
    def create_warning(self, new_warning: Warning) -> Optional[Warning]:
        
        query = """
            INSERT INTO warnings (warning_id, title, description, expire, viewed)
            VALUES (:warning_id, :title, :description, :expire, :viewed)
            RETURNING *;
        """
        
        params = new_warning.model_dump()
            
        result = self.postgres.query(sql=query, params=params)
        
        if not result:
            
            raise Exception("Falha ao criar o aviso, nenhum dado retornado pelo banco")

        created_warning_data = result[0]
        
        return Warning.model_validate(created_warning_data)
    
    def link_to_users(self, user_id: str, warning_id: str) -> None:
        
        query = """
            INSERT INTO user_warning (user_id, warning_id)
            VALUES (:user_id, :warning_id)
        """
        
        params = {"user_id": user_id, "warning_id": warning_id}
        
        self.postgres.query(sql=query, params=params)
        
    def link_to_roles(self, role: ROLE, warning_id: str) -> None:
        
        role_value = role.value
        
        query = """
            INSERT INTO role_warning (role, warning_id)
            VALUES (:role_value, :warning_id)
        """
        
        params = {"role_value": role_value, "warning_id": warning_id}
        
        self.postgres.query(sql=query, params=params)
    
    def update_warning(self, warning_to_update: Warning) -> Optional[Warning]:
        
        query = """
            UPDATE warnings
            SET 
                title = :title,
                description = :description,
                expire = :expire,
                viewed = :viewed
            WHERE
                warning_id = :warning_id
            RETURNING *;
        """
        
        params = warning_to_update.model_dump()
            
        result = self.postgres.query(sql=query, params=params)
        
        if not result:
            
            raise Exception("Falha ao atualizar o aviso, nenhum dado retornado pelo banco")
        
        updated_warning_data = result[0]
        
        return Warning.model_validate(updated_warning_data)
    
    def delete_warning(self, warning_id: str) -> Optional[Warning]:
        
        query = """
            DELETE FROM warnings
            WHERE warning_id = :warning_id
            RETURNING *;
        """
        
        params = {"warning_id": warning_id}
        
        result = self.postgres.query(sql=query, params=params)

        if not result:
            raise Exception("Falha ao deletar o aviso, nenhum dado retornado pelo banco")

        deleted_warning_data = result[0]
        return Warning.model_validate(deleted_warning_data)
    
    def get_warning(self, warning_id: str) -> Optional[Warning]:
        
        query = """
            SELECT * FROM warnings
            WHERE warning_id = :warning_id
            LIMIT 1
        """
        
        params = {"warning_id": warning_id}
        
        result = self.postgres.query(sql=query, params=params)
        
        if not result:
            raise Exception("Falha ao buscar o aviso, nenhum dado retornado pelo banco")
        
        warning_data = result[0]
        
        return Warning.model_validate(warning_data)
    
    def get_all_warnings(self) -> Optional[List[Warning]]:
        
        query = """
            SELECT * FROM warnings
            ORDER BY expire DESC;
        """
        
        results = self.postgres.query(sql=query)
        
        warnings = [Warning.model_validate(data) for data in results]
        
        return warnings
    
    def get_user_warnings(self, user_id: str) -> Optional[List[Warning]]:
        
        query = """
            SELECT w.*
            FROM warnings w
            JOIN user_warning uw ON w.warning_id = uw.warning_id
            WHERE uw.user_id = :user_id
            ORDER BY w.expire DESC;
        """
        
        params = {"user_id": user_id}
        
        results = self.postgres.query(sql=query, params=params)
        
        warnings = [Warning.model_validate(data) for data in results]
        
        return warnings
    
    def get_president_warnings(self) -> Optional[List[Warning]]:
        
        query = """
            SELECT w.*
            FROM warnings w
            JOIN role_warning uw ON w.warning_id = uw.warning_id
            WHERE uw.role = :role
            ORDER BY w.expire DESC;
        """
        
        params = {"role": ROLE.PRESIDENT.value}
        
        results = self.postgres.query(sql=query, params=params)
        
        warnings = [Warning.model_validate(data) for data in results]
        
        return warnings
    