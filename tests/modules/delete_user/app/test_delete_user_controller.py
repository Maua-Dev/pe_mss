from src.modules.delete_user.app.delete_user_controller import DeleteUserController
from src.modules.delete_user.app.delete_user_usecase import DeleteUserUsecase
from src.shared.domain.entities.user import User
from src.shared.domain.enums.course_enum import COURSE
from src.shared.domain.enums.organization_enum import ORGANIZATION
from src.shared.domain.enums.role_enum import ROLE
from src.shared.domain.enums.state_enum import STATE
from src.shared.helpers.external_interfaces.http_models import HttpRequest
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock


class Test_DeleteUserController:
    def test_delete_user_controller_as_self(self):
        repo = UserRepositoryMock()

        usecase = DeleteUserUsecase(repo=repo)
        controller = DeleteUserController(usecase=usecase)

        request = HttpRequest(body={
            'user_id': "550e8400-e29b-41d4-a716-446655440000",
            'user_from_authorizer':{
                'id': '550e8400-e29b-41d4-a716-446655440000',
                'displayName': 'Guilherme',
                'mail': '25.00178-5@maua.br'
            }
        })

        response = controller(request=request)

        assert response.status_code == 200
        assert response.body['user_id'] == "550e8400-e29b-41d4-a716-446655440000"
        assert response.body['message'] == "the user was deleted successfully"
    
    def test_delete_user_controller_as_admin(self):
        repo = UserRepositoryMock()

        usecase = DeleteUserUsecase(repo=repo)
        controller = DeleteUserController(usecase=usecase)

        request = HttpRequest(body={
            'user_id': "550e8400-e29b-41d4-a716-446655440000",
            'user_from_authorizer':{
                'id': '550e8400-e29b-41d4-a716-446655440001',
                'displayName': 'João',
                'mail': '24.00678-2@maua.br'
            }
        })

        response = controller(request=request)

        assert response.status_code == 200
        assert response.body['user_id'] == "550e8400-e29b-41d4-a716-446655440000"
        assert response.body['message'] == "the user was deleted successfully"
    
    def test_delete_member_user_controller_as_president(self):
        repo = UserRepositoryMock()

        usecase = DeleteUserUsecase(repo=repo)
        controller = DeleteUserController(usecase=usecase)

        deleted_user_id = "550e8400-e29b-41d4-a716-446655440089"

        request = HttpRequest(body={
            'user_id': deleted_user_id,
            'user_from_authorizer':{
                'id': "e6bed58f-424a-4b62-b408-18e0a8d1f069",
                'displayName': "Pedro",
                'mail': "20.00789-4@maua.br"
            }
        })

        response = controller(request=request)

        assert response.status_code == 200
        assert response.body['user_id'] == deleted_user_id
        assert response.body['message'] == "the user was deleted successfully"

    def test_delete_user_controller_missing_user_from_authorizer(self):
        repo = UserRepositoryMock()
        usecase = DeleteUserUsecase(repo=repo)
        controller = DeleteUserController(usecase=usecase)

        request = HttpRequest(body={
            'user_id': "550e8400-e29b-41d4-a716-446655440001"
        })

        response = controller(request=request)

        assert response.status_code == 400
        assert response.body == "Field user_from_authorizer is missing"

    def test_delete_user_controller_missing_user_id(self):
        repo = UserRepositoryMock()
        usecase = DeleteUserUsecase(repo=repo)
        controller = DeleteUserController(usecase=usecase)

        request = HttpRequest(body={
            'user_from_authorizer':{
                'id': '550e8400-e29b-41d4-a716-446655440001',
                'displayName': 'João',
                'mail': '24.00678-2@maua.br'
            }
        })

        response = controller(request=request)

        assert response.status_code == 400
        assert response.body == "Field user_id is missing"

    def test_delete_user_controller_invalid_user_id(self):
        repo = UserRepositoryMock()
        usecase = DeleteUserUsecase(repo=repo)
        controller = DeleteUserController(usecase=usecase)

        request = HttpRequest(body={
            'user_id': 3
        })

        response = controller(request=request)

        assert response.status_code == 400