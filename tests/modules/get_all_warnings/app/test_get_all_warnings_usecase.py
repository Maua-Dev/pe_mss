import pytest

from src.modules.get_all_warnings.app.get_all_warnings_usecase import GetAllWarningsUseCase
from src.shared.domain.enums.organization_enum import ORGANIZATION
from src.shared.domain.enums.role_enum import ROLE
from src.shared.helpers.errors.usecase_errors import NoItemsFound
from src.shared.infra.repositories.warning_repository_mock import WarningRepositoryMock
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock


class Test_GetAllWarningsUsecase:
    def test_get_all_warnings_usecase(self):
        repo = WarningRepositoryMock()
        user_repo = UserRepositoryMock()
        usecase = GetAllWarningsUseCase(repo=repo, user_repo=user_repo)
        
        all_warnings = usecase()
        
        assert len(all_warnings) > 0
        assert all_warnings == repo.warnings
        
    def test_get_all_warnings_usecase_multiple_warnings(self):
        repo = WarningRepositoryMock()
        user_repo = UserRepositoryMock()
        usecase = GetAllWarningsUseCase(repo=repo, user_repo=user_repo)
        
        initial_count = len(repo.warnings)
        
        all_warnings = usecase()
        
        assert len(all_warnings) == initial_count
        assert all([warning.warning_id is not None for warning in all_warnings])
        assert all([warning.target_role is not None for warning in all_warnings])
        assert all([warning.body is not None for warning in all_warnings])
        
    def test_get_all_warnings_usecase_empty_repository(self):
        repo = WarningRepositoryMock()
        user_repo = UserRepositoryMock()
        usecase = GetAllWarningsUseCase(repo=repo, user_repo=user_repo)
        
        # Clear all warnings
        repo.warnings = []
        
        with pytest.raises(NoItemsFound) as exc_info:
            usecase()
        
        assert str(exc_info.value.message) == "No items found for warning repository."
