
from src.shared.domain.entities.warning import Warning
from src.shared.domain.enums.role_enum import ROLE
from src.shared.infra.repositories.warning_repository_mock import WarningRepositoryMock
import datetime

class TestWarningRepositoryMock:
    
    def test_create_warning_and_custom_getters(self):
        
        #testa também as novas tabelas e os getters customizados
        
        repo = WarningRepositoryMock()
        
        warning_id = "ab08ea56-37c3-41ef-a5db-b024cf9514ab"
        target_id = "3e841c03-fb0a-4d3e-a726-3768bc0d6726"
        target_role = ROLE.PRESIDENT
        
        new_warning = Warning(
            title="Titulo teste 1",
            description="Descrição teste 1",
            expire=datetime.datetime.now(datetime.UTC),
            viewed=False,
            warning_id=warning_id
        )
        
        created_warning = repo.create_warning(
            new_warning=new_warning,
            target_id=target_id,
            target_role=target_role
        )
        
        assert created_warning == new_warning
        
        #testando os getters nas tabelas diferentes
        assert repo.get_user_warnings(target_id)[-1] == new_warning
        assert repo.get_president_warnings()[-1] == new_warning
        
    def test_delete_warning(self):
        
        repo = WarningRepositoryMock()
        
        warning = repo.warnings[0]
        warning_id = warning.warning_id
        
        deleted_warning = repo.delete_warning(warning_id=warning_id)
        
        assert deleted_warning == warning
        assert len(repo.get_president_warnings()) == 1
        
    def test_update_warning(self):
        
        repo = WarningRepositoryMock()
        
        previous_warning = repo.warnings[0]
        warning_id = previous_warning.warning_id
        
        updated_warning = Warning(
            warning_id=warning_id,
            title="Título atualizado",
            description="Descrição atualizada",
            expire=datetime.datetime.now(datetime.UTC),
            viewed=True
        )
        
        warning = repo.update_warning(warning=updated_warning)
        
        assert warning == updated_warning
        assert updated_warning != previous_warning
        assert repo.warnings[0] == updated_warning
        
    def test_get_all_warnings(self):
        
        repo = WarningRepositoryMock()
        
        assert len(repo.get_all_warnings()) == 2
        
    def test_get_warning(self):
        
        repo = WarningRepositoryMock()
        
        warning = repo.warnings[0]
        id = repo.warnings[0].warning_id
        
        assert repo.get_warning(warning_id=id) == warning
        
    def test_get_president_warnings(self):
        
        repo = WarningRepositoryMock()
        
        assert len(repo.get_president_warnings()) == 2
        
    def test_get_user_warnings(self):
        
        repo = WarningRepositoryMock()
        
        user_id = repo.user_warning[0].user_id
        
        warnings = repo.get_user_warnings(user_id=user_id)
        
        assert len(warnings) == 1
        