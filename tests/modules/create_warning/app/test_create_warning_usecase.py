import pytest
import datetime

from src.modules.create_warning.app.create_warning_usecase import CreateWarningUsecase
from src.shared.domain.enums.organization_enum import ORGANIZATION
from src.shared.domain.enums.role_enum import ROLE
from src.shared.infra.repositories.warning_repository_mock import WarningRepositoryMock
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock


class Test_CreateWarningUsecase:
    def test_create_warning_general_usecase(self):
        repo = WarningRepositoryMock()
        user_repo = UserRepositoryMock()
        usecase = CreateWarningUsecase(repo=repo, user_repo=user_repo)
        
        initial_warnings_count = len(repo.warnings)
        
        created_warning = usecase(
            title="New General Warning",
            description="This is a general warning for all organizations",
            expire='2025-12-31T23:59:59',
            target_role=ROLE.PRESIDENT
        )
        
        assert created_warning.body.title == "New General Warning"
        assert created_warning.body.description == "This is a general warning for all organizations"
        assert created_warning.target_role == "PRESIDENT"
        assert created_warning.target_org is None
        assert created_warning.warning_id is not None
        assert len(repo.warnings) == initial_warnings_count + 1

    def test_create_warning_specific_org_usecase(self):
        repo = WarningRepositoryMock()
        user_repo = UserRepositoryMock()
        usecase = CreateWarningUsecase(repo=repo, user_repo=user_repo)
        
        initial_warnings_count = len(repo.warnings)
        
        created_warning = usecase(
            title="DEV Organization Warning",
            description="This is a warning specifically for DEV organization",
            expire='2025-12-31T23:59:59',
            target_role=ROLE.PRESIDENT,
            target_org=ORGANIZATION.DEV
        )
        
        assert created_warning.body.title == "DEV Organization Warning"
        assert created_warning.body.description == "This is a warning specifically for DEV organization"
        assert created_warning.target_role == "PRESIDENT"
        assert created_warning.target_org == "DEV"
        assert created_warning.warning_id is not None
        assert len(repo.warnings) == initial_warnings_count + 1

    def test_create_warning_for_user_role_usecase(self):
        repo = WarningRepositoryMock()
        user_repo = UserRepositoryMock()
        usecase = CreateWarningUsecase(repo=repo, user_repo=user_repo)
        
        created_warning = usecase(
            title="User Role Warning",
            description="This is a warning for USER role",
            expire='2025-12-31T23:59:59',
            target_role=ROLE.USER,
            target_org=ORGANIZATION.NAWAT
        )
        
        assert created_warning.body.title == "User Role Warning"
        assert created_warning.body.description == "This is a warning for USER role"
        assert created_warning.target_role == "USER"
        assert created_warning.target_org == "NAWAT"
        assert created_warning.created_at is not None

    def test_create_warning_for_adm_role_usecase(self):
        repo = WarningRepositoryMock()
        user_repo = UserRepositoryMock()
        usecase = CreateWarningUsecase(repo=repo, user_repo=user_repo)
        
        created_warning = usecase(
            title="ADM Warning",
            description="Important warning for administrators",
            expire='2025-12-31T23:59:59',
            target_role=ROLE.ADM
        )
        
        assert created_warning.body.title == "ADM Warning"
        assert created_warning.body.description == "Important warning for administrators"
        assert created_warning.target_role == "ADM"
        assert created_warning.target_org is None
