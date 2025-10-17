from urllib import response
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

        expected_users = [
            {
                'user_id': u.user_id,
                'name': u.name,
                'email': u.email,
                'state': (u.state.value if u.state is not None else None),
                'role': (u.role.value if u.role is not None else None),
                'active': (u.active.value if u.active is not None else None),
                'ra': u.ra,
                'course': (u.course.value if u.course is not None else None),
                'year': u.year,
                'organization': (u.organization.value if u.organization is not None else None),
            } 
            for u in sorted(userrepo.get_all_user(), key=lambda x: x.name.casefold())
]
        expected_dict = {
            'users': expected_users,
            'message': 'the users were retrieved'
        }
        assert response.status_code == 200
        assert isinstance(response.body, dict)
        assert len(response.body['users']) == len(expected_users)
        assert response.body == expected_dict

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