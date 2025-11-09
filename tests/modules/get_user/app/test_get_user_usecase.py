import pytest
from src.modules.get_user.app.get_user_usecase import GetUserUsecase
from src.shared.domain.entities.user import User
from src.shared.helpers.errors.usecase_errors import ForbiddenAction, NoItemsFound
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock


class Test_GetUserUsecase:
    def test_get_user_usecase(self):
        user_repo = UserRepositoryMock()
        usecase = GetUserUsecase(user_repo=user_repo)

        user = usecase(user_id="550e8400-e29b-41d4-a716-446655440001")
        assert user == user_repo.users[1]
        assert type(user) == User

    def test_get_user_usecase_not_found_user(self):
        user_repo = UserRepositoryMock()
        usecase = GetUserUsecase(user_repo=user_repo)

        with pytest.raises(NoItemsFound):
            usecase(user_id="550e8400-e29b-41d4-a716-446655440099")

    def test_get_user_usecase_disconnected_user(self):
        user_repo = UserRepositoryMock()
        usecase = GetUserUsecase(user_repo=user_repo)

        with pytest.raises(ForbiddenAction):
            usecase(user_id="3d32ec27-09c3-41da-92e2-be106e449b6a")