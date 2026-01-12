from src.modules.delete_warning.app.delete_warning_controller import DeleteWarningController
from src.modules.delete_warning.app.delete_warning_usecase import DeleteWarningUsecase
from src.shared.helpers.external_interfaces.http_models import HttpRequest
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock
from src.shared.infra.repositories.warning_repository_mock import WarningRepositoryMock


class Test_DeleteWarningUsecase:
    def test_delete_warning_controller_everything_corect(self):
        repo = WarningRepositoryMock()
        user_repo= UserRepositoryMock()
        usecase= DeleteWarningUsecase(repo=repo, user_repo=user_repo)
        controller= DeleteWarningController(usecase=usecase)

        request = HttpRequest(body={
            'user_from_authorizer':{
                'id': '550e8400-e29b-41d4-a716-446655440001',
                'displayName': 'João',
                'mail': '21.00678-2@maua.br'
            },
            'warning_id':'e6112d17-c030-4d65-8b9f-e472d20055a5'
        })

        response= controller(request=request)

        assert response.status_code == 200
        assert response.body["warning"]["warning_id"] == 'e6112d17-c030-4d65-8b9f-e472d20055a5'
        assert response.body["warning"]["target_role"] == 'PRESIDENT'
        assert response.body["warning"]["target_org"] == 'DEV'
        assert response.body["warning"]["body"]["title"] == 'Titulo do alerta 1'
        assert response.body["warning"]["body"]["description"] == 'Descrição do alerta 1'
        assert response.body["warning"]["body"]["expire"] == response.body["warning"]["body"]["expire"]
        assert response.body["warning"]["created_at"] == response.body["warning"]["created_at"]


    def test_delete_warning_with_missing_warning_id(self):
        repo = WarningRepositoryMock()
        user_repo= UserRepositoryMock()
        usecase= DeleteWarningUsecase(repo=repo, user_repo=user_repo)
        controller= DeleteWarningController(usecase=usecase)

        request = HttpRequest(body={
            'user_from_authorizer':{
                'id': '550e8400-e29b-41d4-a716-446655440001',
                'displayName': 'João',
                'mail': '21.00678-2@maua.br'
            }
        })

        response= controller(request=request)

        assert response.status_code == 400
        assert response.body == 'Field warning_id is missing'

    def test_delete_warning_with_nonexistent_warning_id(self):
        repo = WarningRepositoryMock()
        user_repo= UserRepositoryMock()
        usecase= DeleteWarningUsecase(repo=repo, user_repo=user_repo)
        controller= DeleteWarningController(usecase=usecase)

        request = HttpRequest(body={
            'user_from_authorizer':{
                'id': '550e8400-e29b-41d4-a716-446655440001',
                'displayName': 'João',
                'mail': '21.00678-2@maua.br'
            },
            'warning_id':'nothing'
        })

        response= controller(request=request)

        assert response.status_code == 404
        assert response.body == 'No items found for nothing'


    def test_delete_warning_with_wrong_type_warning_id(self):
        repo = WarningRepositoryMock()
        user_repo= UserRepositoryMock()
        usecase= DeleteWarningUsecase(repo=repo, user_repo=user_repo)
        controller= DeleteWarningController(usecase=usecase)

        request = HttpRequest(body={
            'user_from_authorizer':{
                'id': '550e8400-e29b-41d4-a716-446655440001',
                'displayName': 'João',
                'mail': '21.00678-2@maua.br'
            },
            'warning_id':12345
        })

        response= controller(request=request)

        assert response.status_code == 400
        assert response.body == 'Field warning_id isn\'t in the right type.\n Received: int.\n Expected: str'
