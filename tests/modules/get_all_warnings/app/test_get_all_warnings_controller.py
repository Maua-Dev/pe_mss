from src.modules.get_all_warnings.app.get_all_warnings_controller import GetAllWarningsController
from src.modules.get_all_warnings.app.get_all_warnings_usecase import GetAllWarningsUseCase
from src.shared.helpers.external_interfaces.http_models import HttpRequest
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock
from src.shared.infra.repositories.warning_repository_mock import WarningRepositoryMock

class TestGetAllWarningsController:
    def test_get_all_warnings_controller(self):
        repo= WarningRepositoryMock()
        user_repo=  UserRepositoryMock()
        usecase = GetAllWarningsUseCase(repo=repo, user_repo=user_repo)
        controller = GetAllWarningsController(usecase=usecase)

        request = HttpRequest(body={
            'user_from_authorizer':{
                'id': "550e8400-e29b-41d4-a716-446655440001",
                'displayName': "João",
                'mail': "21.00678-2@maua.br"
            }
        })

        response = controller(request=request)

        expected_warnings = [
            {
                'warning': {
                    'body': {
                        'title': w.body.title,
                        'description': w.body.description,
                        'expire': w.body.expire,
                    },
                    'created_at': w.created_at,
                    'target_org': (w.target_org if w.target_org is not None else None),
                    'target_role': w.target_role,
                    'warning_id': w.warning_id,
                }
            }

            for w in sorted(usecase.repo.get_all_warnings(), key=lambda x: x.created_at)
        ]
        expected_dict = {
            'warnings': expected_warnings,
            'message': 'The warnings were retrieved successfully'
        }

        assert response.status_code == 200
        assert isinstance(response.body, dict)
        assert len(response.body['warnings']) == len(expected_warnings)
        assert response.body == expected_dict


    def test_get_all_warnings_controller_missing_user_from_authorizer(self):
        repo= WarningRepositoryMock()
        user_repo=  UserRepositoryMock()
        usecase = GetAllWarningsUseCase(repo=repo, user_repo=user_repo)
        controller = GetAllWarningsController(usecase=usecase)

        request = HttpRequest(body={
        })

        response = controller(request=request)

        assert response.status_code == 400
        assert response.body == 'Field user_from_authorizer is missing'

    def test_get_all_warnings_controller_user_not_adm(self):
        repo= WarningRepositoryMock()
        user_repo=  UserRepositoryMock()
        usecase = GetAllWarningsUseCase(repo=repo, user_repo=user_repo)
        controller = GetAllWarningsController(usecase=usecase)

        request = HttpRequest(body={
            'user_from_authorizer':{
                'id': "550e8400-e29b-41d4-a716-446655440000",
                'displayName': "Guilherme",
                'mail': "25.00178-5@maua.br"
            }
        })

        response = controller(request=request)

        assert response.status_code == 403
        assert response.body == 'Only ADM users can get all warnings.'