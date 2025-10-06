import os
import pytest

from src.shared.domain.enums.organization_enum import ORGANIZATION
from src.shared.domain.enums.role_enum import ROLE
from src.shared.infra.repositories.warning_repository_dynamo import WarningRepositoryDynamo
from src.shared.infra.repositories.warning_repository_mock import WarningRepositoryMock


class Test_WarningRepositoryDynamo:
    IN_GITHUB_ACTIONS = os.getenv('GITHUB_ACTIONS', 'false').lower() == 'true'
    
    @pytest.mark.skipif(IN_GITHUB_ACTIONS, reason="Skipping tests in GitHub Actions environment")
    def test_create_warning(self):
        os.environ["STAGE"] = "TEST"

        warning_repository = WarningRepositoryDynamo()
        warning_repository_mock = WarningRepositoryMock()
        resp = warning_repository.create_warning(warning_repository_mock.warnings[0], ORGANIZATION.DEV, ROLE.PRESIDENT)

        assert resp is not None
        assert resp.title == warning_repository_mock.warnings[0].title

    @pytest.mark.skipif(IN_GITHUB_ACTIONS, reason="Skipping tests in GitHub Actions environment")
    def test_create_warning_invalid(self):
        os.environ["STAGE"] = "TEST"

        warning_repository = WarningRepositoryDynamo()
        warning_repository_mock = WarningRepositoryMock()
        
        with pytest.raises(Exception) as excinfo:
            warning_repository.create_warning(None, ORGANIZATION.DEV, ROLE.PRESIDENT)
        
        assert "object has no attribute" in str(excinfo.value)

    @pytest.mark.skipif(IN_GITHUB_ACTIONS, reason="Skipping tests in GitHub Actions environment")
    def test_get_warning(self): 
        os.environ["STAGE"] = "TEST"

        warning_repository = WarningRepositoryDynamo()
        warning_repository_mock = WarningRepositoryMock()
        warning_repository.create_warning(warning_repository_mock.warnings[0], ORGANIZATION.DEV, ROLE.PRESIDENT)
        resp = warning_repository.get_warning(warning_repository_mock.warnings[0].warning_id)

        assert resp is not None
        assert resp.title == warning_repository_mock.warnings[0].title

    @pytest.mark.skipif(IN_GITHUB_ACTIONS, reason="Skipping tests in GitHub Actions environment")
    def test_get_warning_not_found(self):
        os.environ["STAGE"] = "TEST"

        warning_repository = WarningRepositoryDynamo()
        warning_repository_mock = WarningRepositoryMock()
        
        with pytest.raises(Exception) as excinfo:
            warning_repository.get_warning("non-existent-id")
        
        assert "not found" in str(excinfo.value)
        
    # Update warning
    @pytest.mark.skipif(IN_GITHUB_ACTIONS, reason="Skipping tests in GitHub Actions environment")
    def test_update_warning(self):
        os.environ["STAGE"] = "TEST"

        warning_repository = WarningRepositoryDynamo()
        warning_repository_mock = WarningRepositoryMock()
        resp = warning_repository.update_warning(warning_repository_mock.warnings[0].warning_id, warning_repository_mock.warnings[1])
        assert resp is not None
        assert resp.title == warning_repository_mock.warnings[1].title
        
    @pytest.mark.skipif(IN_GITHUB_ACTIONS, reason="Skipping tests in GitHub Actions environment")
    def test_update_warning_invalid(self):
        os.environ["STAGE"] = "TEST"

        warning_repository = WarningRepositoryDynamo()
        warning_repository_mock = WarningRepositoryMock()
        
        with pytest.raises(Exception) as excinfo:
            warning_repository.update_warning(warning_repository_mock.warnings[0].warning_id, None)
        
        assert "object has no attribute" in str(excinfo.value)

    @pytest.mark.skipif(IN_GITHUB_ACTIONS, reason="Skipping tests in GitHub Actions environment")
    def test_update_warning_not_found(self):
        os.environ["STAGE"] = "TEST"

        warning_repository = WarningRepositoryDynamo()
        warning_repository_mock = WarningRepositoryMock()
        
        with pytest.raises(Exception) as excinfo:
            warning_repository.update_warning("non-existent-id", warning_repository_mock.warnings[1])
        
        assert "not found" in str(excinfo.value)
        
    # Delete warning
    @pytest.mark.skipif(IN_GITHUB_ACTIONS, reason="Skipping tests in GitHub Actions environment")
    def test_delete_warning(self):
        os.environ["STAGE"] = "TEST"

        warning_repository = WarningRepositoryDynamo()
        warning_repository_mock = WarningRepositoryMock()

        warning_repository.create_warning(warning_repository_mock.warnings[1], ORGANIZATION.DEV, ROLE.PRESIDENT)
        resp = warning_repository.delete_warning(warning_repository_mock.warnings[1].warning_id)

        assert resp is not None
        assert resp.title == warning_repository_mock.warnings[1].title
        
    @pytest.mark.skipif(IN_GITHUB_ACTIONS, reason="Skipping tests in GitHub Actions environment")
    def test_delete_warning_not_found(self):
        os.environ["STAGE"] = "TEST"

        warning_repository = WarningRepositoryDynamo()
        
        with pytest.raises(Exception) as excinfo:
            warning_repository.delete_warning("non-existent-id")
        assert "not found" in str(excinfo.value)

    @pytest.mark.skipif(IN_GITHUB_ACTIONS, reason="Skipping tests in GitHub Actions environment")
    def test_get_all_warnings(self):
        os.environ["STAGE"] = "TEST"

        warning_repository = WarningRepositoryDynamo()
        resp = warning_repository.get_all_warnings()
        
        assert resp is not None
        assert isinstance(resp, list)