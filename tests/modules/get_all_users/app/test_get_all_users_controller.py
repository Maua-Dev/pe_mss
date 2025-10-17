from src.modules.get_all_users.app.get_all_users_controller import GetAllUsersController
from src.modules.get_all_users.app.get_all_users_usecase import GetAllUsersUsecase
from src.shared.helpers.external_interfaces.http_models import HttpRequest
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock


class TestGetAllUsersController:

    def test_get_all_users_controller(self):
        userrepo = UserRepositoryMock()
        usecase = GetAllUsersUsecase(userrepo=userrepo)
        controller = GetAllUsersController(usecase=usecase)

        request = HttpRequest(body={
            'user_id': "550e8400-e29b-41d4-a716-446655440001",
            'user_from_authorizer':{
                'id': "550e8400-e29b-41d4-a716-446655440001",
                'displayName': "Guilherme",
                'mail': "25.00178-5@maua.br"
            }
        })

        response = controller(request=request)

        expected_dict = {
            'users': [
                {
                    'name': user.name,
                    'email': user.email,
                    'ra': user.ra,
                    'state': user.state,
                    'role': user.role,
                    'active': user.active,
                    'course': user.course,
                    'year': user.year,
                    'organization': user.organization,
                    'user_id': user.user_id
                } for user in userrepo.get_all_user()
            ],
            'message': 'the users were retrieved'
        }

        assert response.status_code == 200
        assert type(response.body) == list
        assert len(response.body[0]['users']) == 8
        assert all([type(user) == dict for user in response.body[0]['users']])
        assert response.body[0]['message'] == 'the users were retrieved'
        assert response.body[0] == expected_dict

    def test_get_all_users_controller_missing_user_from_authorizer(self):
        userrepo = UserRepositoryMock()
        usecase = GetAllUsersUsecase(userrepo=userrepo)
        controller = GetAllUsersController(usecase=usecase)

        request = HttpRequest(body={
            'user_id': "550e8400-e29b-41d4-a716-446655440001"
        })

        response = controller(request=request)

        assert response.status_code == 400
        assert response.body == 'Field user_from_authorizer is missing'

    def test_get_all_users_controller_wrong_type_parameter(self):
        userrepo = UserRepositoryMock()
        usecase = GetAllUsersUsecase(userrepo=userrepo)
        controller = GetAllUsersController(usecase=usecase)

        request = HttpRequest(body={
            'user_id': "550e8400-e29b-41d4-a716-446655440001",
            'user_from_authorizer':{
                'id': 12345,
                'displayName': "Guilherme",
                'mail': "25.00178-5@maua.br"
            }
        })

        response = controller(request=request)

        assert response.status_code == 400
        assert "Field id isn't in the right type" in response.body
        assert "Received: int" in response.body
        assert "Expected: str" in response.body