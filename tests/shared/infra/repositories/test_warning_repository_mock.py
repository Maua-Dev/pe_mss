
from src.shared.domain.entities.warning import Warning, WarningBody
from src.shared.domain.enums.organization_enum import ORGANIZATION
from src.shared.domain.enums.role_enum import ROLE
from src.shared.infra.repositories.warning_repository_mock import WarningRepositoryMock
import datetime

class TestWarningRepositoryMock:
    
    def test_create_warning(self):
        repo = WarningRepositoryMock()
        
        old_len = len(repo.warnings)
        
        new_warning = Warning(
            target_role=ROLE.PRESIDENT,
            target_org=ORGANIZATION.METAVERSO,
            body=WarningBody(
                title="Titulo do alerta teste",
                description="Descrição do alerta teste",
                expire=datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=7)
            ),
            created_at=datetime.datetime.now(datetime.timezone.utc)
        )

        created_warning = repo.create_warning(new_warning=new_warning)

        assert created_warning == new_warning
        assert len(repo.warnings) == old_len + 1
        
    def test_update_warning(self):
        repo = WarningRepositoryMock()
        
        previous_warning = repo.warnings[0]
        warning_id = previous_warning.warning_id
        
        updated_warning = Warning(
            warning_id=warning_id,
            target_role=ROLE.PRESIDENT,
            target_org=ORGANIZATION.METAVERSO,
            body=WarningBody(
                title="Titulo do alerta atualizado",
                description="Descrição do alerta atualizada",
                expire=datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=15)
            ),
            created_at=previous_warning.created_at
        )
        
        warning = repo.update_warning(warning=updated_warning)
        
        assert warning == updated_warning
        assert updated_warning != previous_warning
        assert repo.warnings[0] == updated_warning
        
    def test_get_all_warnings(self):
        repo = WarningRepositoryMock()
        
        assert len(repo.get_all_warnings()) == 3
        
    def test_get_warning(self):
        repo = WarningRepositoryMock()
        
        warning = repo.warnings[0]
        id = repo.warnings[0].warning_id
        
        assert repo.get_warning(warning_id=id) == warning
        
    def test_get_warnings_by_org(self):
        repo = WarningRepositoryMock()
        
        org = ORGANIZATION.DEV
        
        warnings = repo.get_warnings_by_org(target_org=org)
        
        assert len(warnings) == 1
        assert all(ORGANIZATION(w.target_org) == org for w in warnings)

    def test_get_warnings_by_role(self):
        repo = WarningRepositoryMock()
        
        role = ROLE.PRESIDENT
        
        warnings = repo.get_warnings_by_role(target_role=role)
        
        assert len(warnings) == 3
        assert all(ROLE(w.target_role) == role for w in warnings)

    def test_get_warnings_by_org_and_role(self):
        repo = WarningRepositoryMock()
        
        org = ORGANIZATION.DEV
        role = ROLE.PRESIDENT
        
        warnings = repo.get_warnings_by_org_and_role(target_org=org, target_role=role)
        
        assert len(warnings) == 1
        assert all(ORGANIZATION(w.target_org) == org and ROLE(w.target_role) == role for w in warnings)

    def test_delete_warning(self):
        repo = WarningRepositoryMock()
        
        warning = repo.warnings[0]
        warning_id = warning.warning_id
        
        deleted_warning = repo.delete_warning(warning_id=warning_id)
        
        assert deleted_warning == warning
        assert len(repo.warnings) == 2        