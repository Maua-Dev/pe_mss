from src.modules.update_user.app.update_user_controller import UpdateUserController
from src.modules.update_user.app.update_user_usecase import UpdateUserUsecase
from src.shared.helpers.external_interfaces.http_models import HttpRequest
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock


class Test_UpdateUserControllerOptionalFields:
    def test_update_user_with_course_and_year(self):
        repo = UserRepositoryMock()
        usecase = UpdateUserUsecase(repo=repo)
        controller = UpdateUserController(usecase=usecase)

        request = HttpRequest(body={
            'user_id': repo.users[0].user_id,
            'name': 'User Atualizado',
            'email': repo.users[0].email,
            'ra': repo.users[0].ra,
            'state': repo.users[0].state.name,
            'role': repo.users[0].role.name,
            'course': 'CIC',   # opcional
            'year': 3          # opcional
        })

        response = controller(request=request)

        assert response.status_code == 200
        assert response.body['course'].name == 'CIC'
        assert response.body['year'] == 3

    def test_update_user_with_organization(self):
        repo = UserRepositoryMock()
        usecase = UpdateUserUsecase(repo=repo)
        controller = UpdateUserController(usecase=usecase)

        request = HttpRequest(body={
            'user_id': repo.users[1].user_id,
            'name': 'Outro Nome',
            'email': repo.users[1].email,
            'ra': repo.users[1].ra,
            'state': repo.users[1].state.name,
            'role': repo.users[1].role.name,
            'organization': 'DEV'  # opcional
        })

        response = controller(request=request)

        assert response.status_code == 200
        assert response.body['organization'].name == 'DEV'

    def test_update_user_invalid_course_enum(self):
        repo = UserRepositoryMock()
        usecase = UpdateUserUsecase(repo=repo)
        controller = UpdateUserController(usecase=usecase)

        request = HttpRequest(body={
            'user_id': repo.users[2].user_id,
            'name': 'Teste',
            'email': repo.users[2].email,
            'ra': repo.users[2].ra,
            'state': repo.users[2].state.name,
            'role': repo.users[2].role.name,
            'course': 'INVALIDO'
        })

        response = controller(request=request)

        assert response.status_code == 400
        assert response.body == "Field course is not valid"

    def test_update_user_invalid_year_type(self):
        repo = UserRepositoryMock()
        usecase = UpdateUserUsecase(repo=repo)
        controller = UpdateUserController(usecase=usecase)

        request = HttpRequest(body={
            'user_id': repo.users[2].user_id,
            'name': 'Teste',
            'email': repo.users[2].email,
            'ra': repo.users[2].ra,
            'state': repo.users[2].state.name,
            'role': repo.users[2].role.name,
            'year': "terceiro"  # errado, deveria ser int
        })

        response = controller(request=request)

        assert response.status_code == 400
        assert "Field year isn't in the right type" in response.body

    def test_update_user_invalid_organization_enum(self):
        repo = UserRepositoryMock()
        usecase = UpdateUserUsecase(repo=repo)
        controller = UpdateUserController(usecase=usecase)

        request = HttpRequest(body={
            'user_id': repo.users[2].user_id,
            'name': 'Teste',
            'email': repo.users[2].email,
            'ra': repo.users[2].ra,
            'state': repo.users[2].state.name,
            'role': repo.users[2].role.name,
            'organization': 'INVALIDO'
        })

        response = controller(request=request)

        assert response.status_code == 400
        assert response.body == "Field organization is not valid"
