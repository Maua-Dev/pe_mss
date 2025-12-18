from src.modules.get_warning.app.get_warning_controller import GetWarningController
from src.modules.get_warning.app.get_warning_usecase import GetWarningUsecase
from src.shared.domain.enums.organization_enum import ORGANIZATION
from src.shared.domain.enums.role_enum import ROLE
from src.shared.helpers.external_interfaces.http_models import HttpRequest
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock
from src.shared.infra.repositories.warning_repository_mock import WarningRepositoryMock


class TestGetWarningController:
    def test_get_warning_controller_with_warning_id(self):
        repo = WarningRepositoryMock()
        user_repo = UserRepositoryMock()
        usecase = GetWarningUsecase(repo=repo, user_repo=user_repo)
        controller = GetWarningController(usecase=usecase)

        request = HttpRequest(body={
            'user_from_authorizer':{
                'id': "550e8400-e29b-41d4-a716-446655440001",
                'displayName': "João",
                'mail': "21.00678-2@maua.br"
            },
            'warning_id': "e6112d17-c030-4d65-8b9f-e472d20055a5"
        })

        response = controller(request=request)

        expected_warning= [
            {
                'warning': {
                    'body': {
                        'title': repo.warnings[0].body.title,
                        'description': repo.warnings[0].body.description,
                        'expire': repo.warnings[0].body.expire,
                    },
                    'created_at': repo.warnings[0].created_at,
                    'target_org': (repo.warnings[0].target_org if repo.warnings[0].target_org is not None else None),
                    'target_role': repo.warnings[0].target_role,
                    'warning_id': repo.warnings[0].warning_id,
                }
            }
        ]

        expeted_dict= {
            'warnings': expected_warning,
            'message': "The warning/s was/were retrieved successfully"
        }

        assert response.status_code == 200
        assert isinstance(response.body, dict)
        assert len(response.body['warnings']) == 1
        assert response.body == expeted_dict


    def test_get_warning_controller_with_org_and_role(self):
        repo = WarningRepositoryMock()
        user_repo = UserRepositoryMock()
        usecase = GetWarningUsecase(repo=repo, user_repo=user_repo)
        controller = GetWarningController(usecase=usecase)

        request = HttpRequest(body={
            'user_from_authorizer':{
                'id': "550e8400-e29b-41d4-a716-446655440001",
                'displayName': "João",
                'mail': "21.00678-2@maua.br"
            },
            'role': "PRESIDENT",
            'organization': 'NAWAT'
        })

        response = controller(request=request)

        expected_warning = [
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

            for w in sorted(repo.get_warnings_by_org_and_role(target_org=ORGANIZATION.NAWAT, target_role=ROLE.PRESIDENT), key=lambda x: x.created_at)
            
        ]

        expeted_dict= {
            'warnings': expected_warning,
            'message': "The warning/s was/were retrieved successfully"
        }

        assert response.status_code == 200
        assert isinstance(response.body, dict)
        assert len(response.body['warnings']) == 2
        assert response.body == expeted_dict


    def test_get_warning_controller_missing_user_from_authorizer(self):
        repo = WarningRepositoryMock()
        user_repo = UserRepositoryMock()
        usecase = GetWarningUsecase(repo=repo, user_repo=user_repo)
        controller = GetWarningController(usecase=usecase)

        request = HttpRequest(body={
            'warning_id': "e6112d17-c030-4d65-8b9f-e472d20055a5"
        })

        response = controller(request=request)

        assert response.status_code == 400
        assert response.body == 'Field user_from_authorizer is missing'