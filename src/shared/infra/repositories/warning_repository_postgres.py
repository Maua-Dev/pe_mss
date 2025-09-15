from src.shared.domain.entities.warning import Warning
from src.shared.domain.repositories.warning_repository_interface import IWarningRepository
from src.shared.environments import Environments
from src.shared.infra.external.postgres.datasources.postgres_datasource import RdsDataDatasource


class WarningRepositoryPostgres():
    def __init__(self, db_datasource):
        self.postgres = db_datasource
        
    def create_warning(self, new_warning):
        
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