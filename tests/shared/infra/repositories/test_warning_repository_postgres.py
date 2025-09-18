from src.shared.infra.external.postgres.datasources.postgres_datasource_tests import TestsRdsDatasource
from src.shared.infra.repositories.warning_repository_postgres import WarningRepositoryPostgres
from src.shared.domain.entities.warning import Warning
from src.shared.domain.enums.role_enum import ROLE
import uuid
import datetime
import pytest

class TestWarningRepositoryPostgres:
    
    @pytest.mark.skip("Can't run tests in GitHub actions")
    def test_create_warning_repository_postgres(self):
        
        datasource = TestsRdsDatasource()
        
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
        
    @pytest.mark.skip("Can't run tests in GitHub actions")
    def test_link_to_users_and_retreive(self):
        
        # this tests for get_user_warnings also
        
        datasource = TestsRdsDatasource()
        
        repo = WarningRepositoryPostgres(db_datasource=datasource)
        
        # id do primeiro usuário do banco
        # esse id precisa ser 'válido' e estar presente no banco de usuers
        # pois a chave na tabela link é Foreign
        id = "550e8400-e29b-41d4-a716-446655440000"
        
        new_warning = Warning(
            title="Titulo teste 1",
            description="Descricao teste 1",
            expire=datetime.datetime.now(datetime.UTC),
            viewed=False
        )
        
        repo.create_warning(
            new_warning=new_warning
        )
        
        repo.link_to_users(user_id=id, warning_id=new_warning.warning_id)
        
        warnings = repo.get_user_warnings(user_id=id)
        
        assert new_warning == warnings[0]
        
        datasource.close()
        
    @pytest.mark.skip("Can't run tests in GitHub actions")
    def test_link_to_roles_and_retreive(self):
        
        # this tests for get_president_roles also
        
        datasource = TestsRdsDatasource()
        
        repo = WarningRepositoryPostgres(db_datasource=datasource)
        
        new_warning = Warning(
            title="Titulo teste 1",
            description="Descricao teste 1",
            expire=datetime.datetime.now(datetime.UTC),
            viewed=False
        )
        
        repo.create_warning(
            new_warning=new_warning
        )
        
        repo.link_to_roles(role=ROLE.PRESIDENT, warning_id=new_warning.warning_id)
        
        warnings = repo.get_president_warnings()
        
        found = False
        
        for warning in warnings:
            
            if warning == new_warning:
                
                found = True
                
        assert found == True

        datasource.close()
        
    @pytest.mark.skip("Can't run tests in GitHub actions")
    def test_update_warning(self):
        
        datasource = TestsRdsDatasource()
        
        repo = WarningRepositoryPostgres(db_datasource=datasource)
        
        # primeiro alerta do banco
        # esse id precisa existir no banco
        warning_id_to_update = "e6112d17-c030-4d65-8b9f-e472d20055a5"
        
        updated_warning_entity = Warning(
            warning_id=warning_id_to_update,
            title="Titulo atualizado",
            description="Descrição antiga",
            expire=datetime.datetime.now(datetime.UTC),
            viewed=True
        )
        
        warning = repo.update_warning(warning_to_update=updated_warning_entity)
        
        assert warning == updated_warning_entity
        
        datasource.close()
   
    @pytest.mark.skip("Can't run tests in GitHub actions")    
    def test_delete_warning(self):
        
        datasource = TestsRdsDatasource()
        
        repo = WarningRepositoryPostgres(db_datasource=datasource)
        
        new_warning = Warning(
            title="Titulo teste 1",
            description="Descricao teste 1",
            expire=datetime.datetime.now(datetime.UTC),
            viewed=False
        )
        
        repo.create_warning(new_warning=new_warning)
        
        repo.link_to_roles(role=ROLE.PRESIDENT, warning_id=new_warning.warning_id)
        
        deleted_warning = repo.delete_warning(
            warning_id=new_warning.warning_id
        )
        
        assert deleted_warning == new_warning
        
        # asserting the cascade delete
        # this asserts the following logic: if a warning is created AND linked to anything, then its delete
        # should erase those links due to cascade delete in table creation! (look for it in load_warnings_to_postgrass file)
        
        president_warnings = repo.get_president_warnings()
        
        link_was_deleted = True
        
        for warning in president_warnings:
            
            if warning == new_warning or warning == new_warning.warning_id:
                
                link_was_deleted = False
                
        assert link_was_deleted == True
        
        datasource.close()
        
    @pytest.mark.skip("Can't run tests in GitHub actions")
    def test_get_warning(self):
        
        datasource = TestsRdsDatasource()
        
        repo = WarningRepositoryPostgres(db_datasource=datasource)
        
        new_warning = Warning(
            title="Titulo teste 1",
            description="Descricao teste 1",
            expire=datetime.datetime.now(datetime.UTC),
            viewed=False
        )
        
        repo.create_warning(new_warning=new_warning)
        
        warning = repo.get_warning(warning_id=new_warning.warning_id)
        
        assert warning == new_warning
        
        datasource.close()
        
    @pytest.mark.skip("Can't run tests in GitHub actions")
    def test_get_all_warnings(self):
        
        datasource = TestsRdsDatasource()
        
        repo = WarningRepositoryPostgres(db_datasource=datasource)
        
        new_warning = Warning(
            title="Titulo teste 1",
            description="Descricao teste 1",
            expire=datetime.datetime.now(datetime.UTC),
            viewed=False
        )
        
        prev_len = len(repo.get_all_warnings())
        
        repo.create_warning(new_warning=new_warning)   
        
        post_len = len(repo.get_all_warnings())     
        
        assert prev_len == post_len - 1
        