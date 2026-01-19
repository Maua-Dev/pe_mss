import pytest

from src.modules.get_warning.app.get_warning_usecase import GetWarningUsecase
from src.shared.domain.enums.organization_enum import ORGANIZATION
from src.shared.domain.enums.role_enum import ROLE
from src.shared.helpers.errors.usecase_errors import NoItemsFound
from src.shared.infra.repositories.warning_repository_mock import WarningRepositoryMock
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock


class Test_GetWarningUsecase:
    def test_get_warning_by_id_usecase(self):
        repo = WarningRepositoryMock()
        user_repo = UserRepositoryMock()
        usecase = GetWarningUsecase(repo=repo, user_repo=user_repo)
        
        # Get the first warning from mock
        expected_warning_id = repo.warnings[0].warning_id
        
        warnings = usecase(warning_id=expected_warning_id)
        
        assert len(warnings) == 1
        assert warnings[0].warning_id == expected_warning_id
        assert warnings[0].target_role is not None
        assert warnings[0].body is not None
        
    def test_get_warning_by_role_and_organization_usecase(self):
        repo = WarningRepositoryMock()
        user_repo = UserRepositoryMock()
        usecase = GetWarningUsecase(repo=repo, user_repo=user_repo)
        
        warnings = usecase(role=ROLE.PRESIDENT, organization=ORGANIZATION.DEV)
        
        assert len(warnings) > 0
        # Check that all warnings match the criteria
        for warning in warnings:
            assert warning.target_role == ROLE.PRESIDENT.value
            # Should be either general (no org) or specific to DEV
            if warning.target_org is not None:
                assert warning.target_org == ORGANIZATION.DEV.value
        
    def test_get_warning_by_role_and_organization_nawat_usecase(self):
        repo = WarningRepositoryMock()
        user_repo = UserRepositoryMock()
        usecase = GetWarningUsecase(repo=repo, user_repo=user_repo)
        
        warnings = usecase(role=ROLE.PRESIDENT, organization=ORGANIZATION.NAWAT)
        
        assert len(warnings) > 0
        for warning in warnings:
            assert warning.target_role == ROLE.PRESIDENT.value
            if warning.target_org is not None:
                assert warning.target_org == ORGANIZATION.NAWAT.value
                
    def test_get_warning_not_found_usecase(self):
        repo = WarningRepositoryMock()
        user_repo = UserRepositoryMock()
        usecase = GetWarningUsecase(repo=repo, user_repo=user_repo)
        
        with pytest.raises(NoItemsFound):
            usecase(warning_id="non-existent-warning-id")
            
    def test_get_warning_returns_list_usecase(self):
        repo = WarningRepositoryMock()
        user_repo = UserRepositoryMock()
        usecase = GetWarningUsecase(repo=repo, user_repo=user_repo)
        
        # Test with warning_id returns a list
        warning_id = repo.warnings[0].warning_id
        result = usecase(warning_id=warning_id)
        
        assert isinstance(result, list)
        assert len(result) >= 1
        
    def test_get_warning_by_role_and_org_returns_list_usecase(self):
        repo = WarningRepositoryMock()
        user_repo = UserRepositoryMock()
        usecase = GetWarningUsecase(repo=repo, user_repo=user_repo)
        
        result = usecase(role=ROLE.PRESIDENT, organization=ORGANIZATION.DEV)
        
        assert isinstance(result, list)
        assert len(result) > 0
