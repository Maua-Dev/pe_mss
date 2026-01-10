import pytest

from src.modules.delete_warning.app.delete_warning_usecase import DeleteWarningUsecase
from src.shared.helpers.errors.usecase_errors import ForbiddenAction, NoItemsFound
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock
from src.shared.infra.repositories.warning_repository_mock import WarningRepositoryMock


class Test_DeleteWarningUsecase:
    def test_delete_warning_usecase(self):
        repo = WarningRepositoryMock()
        user_repo = UserRepositoryMock()
        usecase = DeleteWarningUsecase(repo=repo, user_repo=user_repo)

        deleted_warning= usecase(
            warning_id="e6112d17-c030-4d65-8b9f-e472d20055a5",
            user_id="550e8400-e29b-41d4-a716-446655440001"
        )

        assert deleted_warning.warning_id == "e6112d17-c030-4d65-8b9f-e472d20055a5"
        assert deleted_warning.target_role == "PRESIDENT"
        assert deleted_warning.target_org == "DEV"
        assert deleted_warning.body.title == "Titulo do alerta 1"
        assert deleted_warning.body.description == "Descrição do alerta 1"
        assert deleted_warning.body.expire == deleted_warning.body.expire
        assert deleted_warning.created_at == deleted_warning.created_at

    def test_delete_warning_usecase_non_admin_user(self):
        repo = WarningRepositoryMock()
        user_repo = UserRepositoryMock()
        usecase = DeleteWarningUsecase(repo=repo, user_repo=user_repo)

        with pytest.raises(ForbiddenAction) as exc_info:
            usecase(
                warning_id="e6112d17-c030-4d65-8b9f-e472d20055a5",
                user_id="550e8400-e29b-41d4-a716-446655440000"  # Non-admin user
            )
        
        assert str(exc_info.value) == "Only ADM users can delete warnings."

    def test_delete_warning_usecase_warning_not_found(self):
        repo = WarningRepositoryMock()
        user_repo = UserRepositoryMock()
        usecase = DeleteWarningUsecase(repo=repo, user_repo=user_repo)

        with pytest.raises(NoItemsFound) as exc_info:
            usecase(
                warning_id="nonexistent-warning-id",
                user_id="550e8400-e29b-41d4-a716-446655440001"  # Admin user
            )
        
        assert str(exc_info.value) == "No items found for nonexistent-warning-id"

    