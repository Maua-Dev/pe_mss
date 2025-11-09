from src.modules.get_user.app.get_user_controller import GetUserController
from src.modules.get_user.app.get_user_usecase import GetUserUsecase
from src.shared.helpers.external_interfaces.http_models import HttpRequest
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock


class Test_GetUserController:
    user_repo = UserRepositoryMock()
    usecase = GetUserUsecase(user_repo=user_repo)
    controller = GetUserController(usecase=usecase)

    def test_get_user_controller(self):
        request = HttpRequest(body={
            'user_from_authorizer':{
                'id': "550e8400-e29b-41d4-a716-446655440001",
                'displayName': "Guilherme",
                'mail': "25.00178-5@maua.br"
            }
        })

        expected = {
            'user':{
                'user_id': '550e8400-e29b-41d4-a716-446655440001',
                'name': 'João',
                'email': '21.00678-2@maua.br',
                'ra': '21.00678-2',
                'state': 'APPROVED',
                'role': 'ADM',
                'active': 'ACTIVE',
                'course': 'CIC',
                'year': 4,
                'organization': 'DEV'
            },
            'message': 'the user was retrieved'
        }

        response = self.controller(request=request)

        assert response.status_code == 200
        assert response.body == expected

    def test_get_user_controller_invalid_id(self):
        request = HttpRequest(body={
            'user_from_authorizer':{
                'id': "Um id inválido",
                'displayName': "Guilherme",
                'mail': "25.00178-5@maua.br"
            }
        })

        response = self.controller(request=request)

        assert response.status_code == 400

    def test_get_user_controller_without_id(self):
        request = HttpRequest(body={
            'user_from_authorizer':{
                'id': None,
                'displayName': "Guilherme",
                'mail': "25.00178-5@maua.br"
            }
        })

        response = self.controller(request=request)

        assert response.status_code == 400

    def test_get_user_controller_not_found(self):
        request = HttpRequest(body={
            'user_from_authorizer':{
                'id': "550e8400-e29b-41d4-a716-446655440999",
                'displayName': "Guilherme",
                'mail': "25.00178-5@maua.br"
            }
        })

        response = self.controller(request=request)

        assert response.status_code == 400
        assert response.body == "No items found for 550e8400-e29b-41d4-a716-446655440999"