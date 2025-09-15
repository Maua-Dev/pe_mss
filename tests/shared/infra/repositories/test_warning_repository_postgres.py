from src.shared.infra.external.postgres.datasources.postgre_tests_datasource import PostgresTestDatasource
from src.shared.infra.repositories.warning_repository_postgres import WarningRepositoryPostgres
from src.shared.domain.entities.warning import Warning
import datetime

class TestWarningRepositoryPostgres:
    
    def test_create_warning_repository_postgres(self):
        
        datasource = PostgresTestDatasource()
        
        repo = WarningRepositoryPostgres(db_datasource=datasource)
        
        new_warning = Warning(
            title="Titulo teste 1",
            description="Descricao teste 1",
            expire=datetime.datetime.now(datetime.UTC),
            viewed=False
        )
        
        created_warning = repo.create_warning(
            new_warning=new_warning
        )
        
        assert created_warning is not None
        assert created_warning.title == new_warning.title
        
        datasource.close()
        
        
        