import pytest

from src.modules.create_user.app.create_user_usecase import CreateUserUsecase
from src.modules.update_user.app.update_user_usecase import UpdateUserUsecase
from src.shared.domain.enums.course_enum import COURSE
from src.shared.domain.enums.organization_enum import ORGANIZATION
from src.shared.domain.enums.role_enum import ROLE
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock


class Test_CreateUserUsecase:
    def test_create_user_as_admin_usecase(self):
        repo = UserRepositoryMock()
        usecase = CreateUserUsecase(repo=repo)
        created_user = usecase(user_data={
            'new_user': {
                'name': 'Maria',
                'email': '21.00100-2@maua.br',
                'organization': ORGANIZATION.DEV,
                'role': ROLE.USER
            },
        }, case=ROLE.ADM,
            requester_id='550e8400-e29b-41d4-a716-446655440001')
        
        assert created_user.name == 'Maria'
        assert created_user.email == '21.00100-2@maua.br'
        assert created_user.organization == ORGANIZATION.DEV
        assert created_user.role == ROLE.USER

    def test_create_user_as_president_usecase(self):
        repo = UserRepositoryMock()
        usecase = CreateUserUsecase(repo=repo)
        created_user = usecase(user_data={
            'new_user': {
                'name': 'Carlos',
                'email': '21.00100-2@maua.br',
                'organization': ORGANIZATION.NAWAT,
                'role': ROLE.USER,
                'course': COURSE.CIC,
                'year': 4
            },
        }, case=ROLE.PRESIDENT,
            requester_id='550e8400-e29b-41d4-a716-446655440002')

        assert created_user.name == 'Carlos'
        assert created_user.email == '21.00100-2@maua.br'
        assert created_user.organization == ORGANIZATION.NAWAT
        assert created_user.role == ROLE.USER

    def test_create_users_as_admin_usecase(self):
        repo = UserRepositoryMock()
        usecase = CreateUserUsecase(repo=repo)
        created_users = usecase(user_data={
            'new_user': [
                {
                    'name': 'Maria',
                    'email': '21.00100-2@maua.br',
                    'organization': ORGANIZATION.DEV,
                    'role': ROLE.USER
                },
                {
                    'name': 'Carlos',
                    'email': '21.00100-2@maua.br',
                    'organization': ORGANIZATION.NAWAT,
                    'role': ROLE.USER
                }
            ]
        }, case="planilha",
            requester_id='550e8400-e29b-41d4-a716-446655440001')

        assert len(created_users) == 2
        assert created_users[0].name == 'Maria'
        assert created_users[0].email == '21.00100-2@maua.br'
        assert created_users[0].organization == ORGANIZATION.DEV
        assert created_users[0].role == ROLE.USER

        assert created_users[1].name == 'Carlos'
        assert created_users[1].email == '21.00100-2@maua.br'
        assert created_users[1].organization == ORGANIZATION.NAWAT
        assert created_users[1].role == ROLE.USER