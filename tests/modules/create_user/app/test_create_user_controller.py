import pytest
from src.modules.create_user.app.create_user_controller import CreateUserController
from src.modules.create_user.app.create_user_usecase import CreateUserUsecase
from src.shared.domain.enums.course_enum import COURSE
from src.shared.domain.enums.organization_enum import ORGANIZATION
from src.shared.domain.enums.role_enum import ROLE
from src.shared.helpers.external_interfaces.http_codes import BadRequest
from src.shared.helpers.external_interfaces.http_models import HttpRequest
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock


class Test_CreateUserController:
    def test_create_user_controller_wihout_user_from_authorizer(self):
        repo = UserRepositoryMock()
        usecase= CreateUserUsecase(repo=repo)
        controller= CreateUserController(usecase=usecase)

        request = HttpRequest()

        response = controller(request=request)

        assert response.status_code == 400
        assert response.body == 'Field user_from_authorizer is missing'

    def test_create_user_controller_without_new_user(self):
        repo = UserRepositoryMock()
        usecase= CreateUserUsecase(repo=repo)
        controller= CreateUserController(usecase=usecase)

        request = HttpRequest(body={
            'user_from_authorizer':{
                'id': '550e8400-e29b-41d4-a716-446655440001',
                'displayName': 'João',
                'mail': '21.00678-2@maua.br'
            },
        })

        response = controller(request=request)

        assert response.status_code == 400
        assert response.body == 'Field new_user is missing'

    def test_create_user_controller_as_admin(self):
        repo = UserRepositoryMock()
        usecase= CreateUserUsecase(repo=repo)
        controller= CreateUserController(usecase=usecase)

        request = HttpRequest(body={
            'user_from_authorizer':{
                'id': '550e8400-e29b-41d4-a716-446655440001',
                'displayName': 'João',
                'mail': '21.00678-2@maua.br'
            },
            'new_user':{
                'name': 'Maria',
                'email': '21.00100-2@maua.br',
                'organization': ORGANIZATION.DEV,
                'role': ROLE.USER
            }
        })

        response = controller(request=request)

        assert response.status_code == 200
        assert response.body['user_id'] is not None
        assert response.body['name'] == 'Maria'
        assert response.body['email'] == '21.00100-2@maua.br'
        assert response.body['organization'] == 'DEV'
        assert response.body['role'] == 'USER'
        assert response.body['active'] == 'ACTIVE'
        assert response.body['state'] == 'PENDING'
        assert response.body['ra'] == '21.00100-2'

    def test_create_user_controller_as_president(self):
        repo = UserRepositoryMock()
        usecase= CreateUserUsecase(repo=repo)
        controller= CreateUserController(usecase=usecase)

        request = HttpRequest(body={
            'user_from_authorizer':{
                'id': '550e8400-e29b-41d4-a716-446655440002',
                'displayName': 'Heitor',
                'mail': '21.00453-7@maua.br'
            },
            'new_user':{
                'name': 'Maria',
                'email': '21.00100-2@maua.br',
                'organization': ORGANIZATION.NAWAT,
                'role': ROLE.USER,
                'course': COURSE.CIC,
                'year': 4
            }
        })

        response = controller(request=request)

        assert response.status_code == 200
        assert response.body['user_id'] is not None
        assert response.body['name'] == 'Maria'
        assert response.body['email'] == '21.00100-2@maua.br'
        assert response.body['organization'] == 'NAWAT'
        assert response.body['role'] == 'USER'
        assert response.body['active'] == 'ACTIVE'
        assert response.body['state'] == 'PENDING'
        assert response.body['ra'] == '21.00100-2'

    def test_create_user_controller_as_unauthorized_president(self):
        repo = UserRepositoryMock()
        usecase= CreateUserUsecase(repo=repo)
        controller= CreateUserController(usecase=usecase)

        request = HttpRequest(body={
            'user_from_authorizer':{
                'id': '550e8400-e29b-41d4-a716-446655440002',
                'displayName': 'Heitor',
                'mail': '21.00453-7@maua.br'
            },
            'new_user':{
                'name': 'Maria',
                'email': '21.00100-2@maua.br',
                'organization': ORGANIZATION.DEV,
                'role': ROLE.USER,
                'course': COURSE.CIC,
                'year': 4
            }
        })

        response = controller(request=request)

        assert response.status_code == 500
        assert response.body == 'President is not allowed to perform action in other organization besides he\'s'

    def test_create_users_from_spreadsheet_as_admin(self):
        repo = UserRepositoryMock()
        usecase= CreateUserUsecase(repo=repo)
        controller= CreateUserController(usecase=usecase)

        request = HttpRequest(body={
            'user_from_authorizer':{
                'id': '550e8400-e29b-41d4-a716-446655440001',
                'displayName': 'João',
                'mail': '21.00678-2@maua.br'
            },
            'new_user': [
                {
                    'name': 'Maria',
                    'email': '21.00100-2@maua.br',
                    'organization': ORGANIZATION.DEV,
                    'role': ROLE.USER,
                    'course': COURSE.CIC,
                    'year': 4
                },
                {
                    'name': 'José',
                    'email': '21.00101-2@maua.br',
                    'organization': ORGANIZATION.DEV,
                    'role': ROLE.USER,
                    'course': COURSE.CIC,
                    'year': 4
                }
            ]
        })

        response = controller(request=request)

        assert response.status_code == 200
        assert len(response.body) == 2
        assert response.body[0]['user_id'] is not None
        assert response.body[0]['name'] == 'Maria'
        assert response.body[0]['email'] == '21.00100-2@maua.br'
        assert response.body[0]['organization'] == 'DEV'
        assert response.body[0]['role'] == 'USER'
        assert response.body[0]['active'] == 'ACTIVE'
        assert response.body[0]['state'] == 'PENDING'
        assert response.body[0]['ra'] == '21.00100-2'
        assert response.body[1]['user_id'] is not None
        assert response.body[1]['name'] == 'José'
        assert response.body[1]['email'] == '21.00101-2@maua.br'
        assert response.body[1]['organization'] == 'DEV'
        assert response.body[1]['role'] == 'USER'
        assert response.body[1]['active'] == 'ACTIVE'
        assert response.body[1]['state'] == 'PENDING'
        assert response.body[1]['ra'] == '21.00101-2'