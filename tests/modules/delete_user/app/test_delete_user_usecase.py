import pytest
from src.modules.delete_user.app.delete_user_usecase import DeleteUserUsecase
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock


class Test_DeleteUserUsecase:
    def test_delete_user_usecase(self):
        repo = UserRepositoryMock()
        deleted_user_id=repo.users[0].user_id
        usecase = DeleteUserUsecase(repo=repo)
        deleted_user = usecase(user_id=deleted_user_id)

        assert deleted_user.user_id == deleted_user_id
        assert deleted_user.state.value == "PENDING"

    def test_delete_user_usecase_entity_error(self):
        repo = UserRepositoryMock()
        usecase = DeleteUserUsecase(repo=repo)

        with pytest.raises(EntityError):
            usecase(user_id=10)