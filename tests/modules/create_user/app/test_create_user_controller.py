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
        assert response.body["user"]['user_id'] is not None
        assert response.body["user"]['name'] == 'Maria'
        assert response.body["user"]['email'] == '21.00100-2@maua.br'
        assert response.body["user"]['organization'] == 'DEV'
        assert response.body["user"]['role'] == 'USER'
        assert response.body["user"]['active'] == 'ACTIVE'
        assert response.body["user"]['state'] == 'PENDING'
        assert response.body["user"]['ra'] == '21.00100-2'

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
        assert response.body["user"]['user_id'] is not None
        assert response.body["user"]['name'] == 'Maria'
        assert response.body["user"]['email'] == '21.00100-2@maua.br'
        assert response.body["user"]['organization'] == 'NAWAT'
        assert response.body["user"]['role'] == 'USER'
        assert response.body["user"]['active'] == 'ACTIVE'
        assert response.body["user"]['state'] == 'PENDING'
        assert response.body["user"]['ra'] == '21.00100-2'

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

        assert response.status_code == 403
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
        assert response.body["users"][0]['user']['user_id'] is not None
        assert response.body["users"][0]['user']['name'] == 'Maria'
        assert response.body["users"][0]['user']['email'] == '21.00100-2@maua.br'
        assert response.body["users"][0]['user']['organization'] == 'DEV'
        assert response.body["users"][0]['user']['role'] == 'USER'
        assert response.body["users"][0]['user']['active'] == 'ACTIVE'
        assert response.body["users"][0]['user']['state'] == 'PENDING'
        assert response.body["users"][0]['user']['ra'] == '21.00100-2'
        assert response.body["users"][1]['user']['user_id'] is not None
        assert response.body["users"][1]['user']['name'] == 'José'
        assert response.body["users"][1]['user']['email'] == '21.00101-2@maua.br'
        assert response.body["users"][1]['user']['organization'] == 'DEV'
        assert response.body["users"][1]['user']['role'] == 'USER'
        assert response.body["users"][1]['user']['active'] == 'ACTIVE'
        assert response.body["users"][1]['user']['state'] == 'PENDING'
        assert response.body["users"][1]['user']['ra'] == '21.00101-2'