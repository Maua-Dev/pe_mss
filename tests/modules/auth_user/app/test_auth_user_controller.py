import pytest
from src.modules.auth_user.app.auth_user_controller import AuthUserController
from src.modules.auth_user.app.auth_user_usecase import AuthUserUsecase
from src.shared.helpers.external_interfaces.http_codes import BadRequest
from src.shared.helpers.external_interfaces.http_models import HttpRequest
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock


class Test_AuthUserController:
    def test_auth_user_controller_user_is_in_repo_mock(self):
        repo = UserRepositoryMock()
        usecase= AuthUserUsecase(repo=repo)
        controller= AuthUserController(usecase=usecase)

        request = HttpRequest(body={
            'user_from_authorizer':{
                'id': '550e8400-e29b-41d4-a716-446655440000',
                'displayName': 'Guilherme',
                'mail': '25.00178-5@maua.br'
            }
        })

        response = controller(request=request)

        assert response.status_code == 200
        assert response.body["user"]['user_id'] == '550e8400-e29b-41d4-a716-446655440000'
        assert response.body["user"]['name'] == 'Guilherme'
        assert response.body["user"]['email'] == '25.00178-5@maua.br'
        assert response.body["user"]['ra'] == '25.00178-5'
        assert response.body["user"]['state'] == 'PENDING'
        assert response.body["user"]['role'] == 'USER'
        assert response.body["user"]['active'] == 'ACTIVE'
        assert response.body["message"] == 'the user was retrieved successfully'


    def test_auth_user_controller_user_not_in_repo_mock(self):
        repo = UserRepositoryMock()
        usecase= AuthUserUsecase(repo=repo)
        controller= AuthUserController(usecase=usecase)

        request = HttpRequest(body={
            'user_from_authorizer':{
                'id': '550e8400-e29b-41d4-a716-446655440010',
                'displayName': 'José',
                'mail': '20.00158-5@maua.br'
            }
        })

        response= controller(request=request)

        assert response.status_code == 200
        assert response.body["user"]['user_id'] == '550e8400-e29b-41d4-a716-446655440010'
        assert response.body["user"]['name'] == 'José'
        assert response.body["user"]['email'] == '20.00158-5@maua.br'
        assert response.body["user"]['ra'] == '20.00158-5'
        assert response.body["user"]['state'] == None
        assert response.body["user"]['role'] == 'USER'
        assert response.body["user"]['active'] == None
        assert response.body["message"] == 'the user was created successfully'

    def test_auth_user_controller_user_is_in_repo_mock_however_the_request_only_have_id_like_in_repo(self):
        repo = UserRepositoryMock()
        usecase= AuthUserUsecase(repo=repo)
        controller= AuthUserController(usecase=usecase)

        request = HttpRequest(body={
            'user_from_authorizer': {
                'id': '550e8400-e29b-41d4-a716-446655440000',
                'displayName': 'Aurélio',
                'mail': '24.00564-5@maua.br'
            }
        })

        response= controller(request=request)

        assert response.status_code == 200
        assert response.body["user"]['user_id'] == '550e8400-e29b-41d4-a716-446655440000'
        assert response.body["user"]['name'] == 'Aurélio'
        assert response.body["user"]['email'] == '24.00564-5@maua.br'
        assert response.body["user"]['ra'] == '24.00564-5'
        assert response.body["user"]['state'] == None
        assert response.body["user"]['role'] == 'USER'
        assert response.body["user"]['active'] == None
        assert response.body["message"] == 'the user was created successfully'

    def test_auth_user_controller_id_is_missing(self):
        repo = UserRepositoryMock()
        usecase= AuthUserUsecase(repo=repo)
        controller= AuthUserController(usecase=usecase)

        request = HttpRequest(body={
            'user_from_authorizer':{
                'displayName': 'Aurélio',
                'mail': '24.00564-5@maua.br'
            }
        })
        
        response= controller(request=request)

        assert response.status_code == 400
        assert response.body == 'Field id is missing'

    def test_auth_user_controller_display_display_name_is_missing(self):
        repo = UserRepositoryMock()
        usecase= AuthUserUsecase(repo=repo)
        controller= AuthUserController(usecase=usecase)

        request = HttpRequest(body={
            'user_from_authorizer':{
                'id': '550e8400-e29b-41d4-a716-446655440000',
                'mail': '24.00564-5@maua.br'
            }
        })

        response= controller(request=request)

        assert response.status_code == 400
        assert response.body == 'Field displayName is missing'

    def test_auth_user_controller_email_is_missing(self):
        repo = UserRepositoryMock()
        usecase= AuthUserUsecase(repo=repo)
        controller= AuthUserController(usecase=usecase)

        request = HttpRequest(body={
            'user_from_authorizer':{
                'id': '550e8400-e29b-41d4-a716-446655440000',
                'displayName': 'Aurélio'
            }
        })

        response= controller(request=request)

        assert response.status_code == 400
        assert response.body == 'Field mail is missing'

    def test_auth_user_controller_id_is_not_of_type_str(self):
        repo = UserRepositoryMock()
        usecase= AuthUserUsecase(repo=repo)
        controller= AuthUserController(usecase=usecase)

        request = HttpRequest(body={
            'user_from_authorizer':{
                'id': 123456789,
                'displayName': 'Aurélio',
                'mail': '24.00564-5@maua.br'
            }
        })

        response= controller(request=request)

        assert response.status_code == 400
        assert response.body == 'Field id isn\'t in the right type.\n Received: int.\n Expected: str'

    def test_auth_user_controller_display_name_is_not_of_type_str(self):
        repo = UserRepositoryMock()
        usecase= AuthUserUsecase(repo=repo)
        controller= AuthUserController(usecase=usecase)

        request = HttpRequest(body={
            'user_from_authorizer':{
                'id': '550e8400-e29b-41d4-a716-446655440000',
                'displayName': 12345,
                'mail': '24.00564-5@maua.br'
            }
        })

        response= controller(request=request)

        assert response.status_code == 400
        assert response.body == 'Field displayName isn\'t in the right type.\n Received: int.\n Expected: str'


    def test_auth_user_controller_mail_is_not_of_type_str(self):
        repo = UserRepositoryMock()
        usecase= AuthUserUsecase(repo=repo)
        controller= AuthUserController(usecase=usecase)

        request = HttpRequest(body={
            'user_from_authorizer':{
                'id': '550e8400-e29b-41d4-a716-446655440000',
                'displayName': 'Aurélio',
                'mail': 12345
            }
        })

        response= controller(request=request)

        assert response.status_code == 400
        assert response.body == 'Field mail isn\'t in the right type.\n Received: int.\n Expected: str'



    def test_auth_user_controller_id_is_not_on_uud_format(self):
        repo = UserRepositoryMock()
        usecase= AuthUserUsecase(repo=repo)
        controller= AuthUserController(usecase=usecase)

        request = HttpRequest(body={
            'user_from_authorizer':{
                'id': '123456789',
                'displayName': 'Aurélio',
                'mail': '24.00564-5@maua.br'
            }
        })

        response= controller(request=request)

        assert response.status_code == 400
        assert response.body == 'Invalid format for user id'