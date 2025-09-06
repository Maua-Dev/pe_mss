import pytest

from src.modules.auth_user.app.auth_user_usecase import AuthUserUsecase
from src.shared.domain.entities.user import User
from src.shared.domain.enums.active_enum import ACTIVE
from src.shared.domain.enums.role_enum import ROLE
from src.shared.domain.enums.state_enum import STATE
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock

class Test_AuthUserUsecase:
    def test_auth_user_usecase_user_is_in_repo_mock(self):
        repo= UserRepositoryMock()
        usecase= AuthUserUsecase(repo=repo)
        posible_new_user= User(
            user_id="550e8400-e29b-41d4-a716-446655440000",
            name="Guilherme",
            email="25.00178-5@maua.br", 
            state=STATE.PENDING, 
            role=ROLE.USER,
            active=ACTIVE.ACTIVE
        )
        returned_user= usecase(user=posible_new_user)

        assert returned_user[1] == 0
        assert returned_user[0].user_id == "550e8400-e29b-41d4-a716-446655440000"
        assert returned_user[0].name == "Guilherme"


    def test_auth_user_usecase_user_not_in_repo_mock(self):
        repo= UserRepositoryMock()
        usecase= AuthUserUsecase(repo=repo)
        posible_new_user= User(
            user_id="550e8400-e29b-41d4-a716-446655440010",
            name="José",
            email="20.00158-5@maua.br", 
            state=STATE.PENDING, 
            role=ROLE.USER,
            active=ACTIVE.ACTIVE
        )
        returned_user= usecase(user=posible_new_user)

        assert returned_user[1] == 1
        assert returned_user[0].user_id == "550e8400-e29b-41d4-a716-446655440010"
        assert returned_user[0].name == "José"

