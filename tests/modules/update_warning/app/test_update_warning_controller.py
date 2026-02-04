from src.modules.update_warning.app.update_warning_controller import UpdateWarningController
from src.modules.update_warning.app.update_warning_usecase import UpdateWarningUsecase
from src.shared.domain.enums.role_enum import ROLE
from src.shared.domain.enums.organization_enum import ORGANIZATION
from src.shared.helpers.external_interfaces.http_models import HttpRequest
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock
from src.shared.infra.repositories.warning_repository_mock import WarningRepositoryMock
from src.shared.domain.entities.warning import Warning, WarningBody


class Test_UpdateWarningController:
    def test_update_warning_controller_without_user_from_authorizer(self):
        repo = WarningRepositoryMock()
        user_repo= UserRepositoryMock()
        usecase= UpdateWarningUsecase(repo=repo, user_repo=user_repo)
        controller= UpdateWarningController(usecase=usecase)

        request = HttpRequest()

        response = controller(request=request)

        assert response.status_code == 400
        assert response.body == 'Field user_from_authorizer is missing'

    def test_update_warning_controller_without_warning_id(self):
        repo = WarningRepositoryMock()
        user_repo= UserRepositoryMock()
        usecase= UpdateWarningUsecase(repo=repo, user_repo=user_repo)
        controller= UpdateWarningController(usecase=usecase)

        request = HttpRequest(body={
            'user_from_authorizer':{
                'id': '550e8400-e29b-41d4-a716-446655440001',
                'displayName': 'João',
                'mail': '21.00678-2@maua.br',
            },
            'update_warning':{
                'updated_warning':{
                    'title': 'Atualização de sistema - versão 2',
                    'description': 'O sistema será atualizado no próximo fim de semana. Esta é a versão 2.',
                },
            }
        })

        response= controller(request=request)
        assert response.status_code == 400
        assert response.body == 'Field warning_id is missing'

    def test_update_warning_controller_with_specific_warning_and_as_admin(self):
        repo = WarningRepositoryMock()
        user_repo= UserRepositoryMock()
        usecase= UpdateWarningUsecase(repo=repo, user_repo=user_repo)
        controller= UpdateWarningController(usecase=usecase)

        new_warning: Warning = Warning(
            target_role=ROLE.USER,
            target_org=ORGANIZATION.DEV,
            body=WarningBody(
                title='Atualização de sistema',
                description='O sistema será atualizado no próximo fim de semana.',
                expire=1704067200000
            ),
            created_at=1672531200000
        )

        warning = usecase.repo.create_warning(new_warning)

        request = HttpRequest(body={
            'user_from_authorizer':{
                'id': '550e8400-e29b-41d4-a716-446655440001',
                'displayName': 'João',
                'mail': '21.00678-2@maua.br',
            },
            'update_warning':{
                'warning_id': warning.warning_id,
                'updated_warning':{
                    'title': 'Atualização de sistema - versão 2',
                    'description': 'O sistema será atualizado no próximo fim de semana. Esta é a versão 2.',
                },
            }
        })

        response= controller(request=request)
        assert response.status_code == 200
        assert response.body["updated_warning"]['warning_id'] == warning.warning_id
        assert response.body["updated_warning"]['body']['title'] == 'Atualização de sistema - versão 2'
        assert response.body["updated_warning"]['body']['description'] == 'O sistema será atualizado no próximo fim de semana. Esta é a versão 2.'

    def test_update_warning_controller_with_nonexistent_warning_id(self):
        repo = WarningRepositoryMock()
        user_repo= UserRepositoryMock()
        usecase= UpdateWarningUsecase(repo=repo, user_repo=user_repo)
        controller= UpdateWarningController(usecase=usecase)

        request = HttpRequest(body={
            'user_from_authorizer':{
                'id': '550e8400-e29b-41d4-a716-446655440001',
                'displayName': 'João',
                'mail': '21.00678-2@maua.br',
            },
            'update_warning':{
                'warning_id': 'nonexistent-warning-id',
                'updated_warning':{
                    'title': 'Atualização de sistema - versão 2',
                    'description': 'O sistema será atualizado no próximo fim de semana. Esta é a versão 2.',
                },
            }
        })

        response= controller(request=request)
        assert response.status_code == 404
        assert response.body == 'No items found for nonexistent-warning-id'

    def test_update_warning_controller_with_insufficient_permissions(self):
        repo = WarningRepositoryMock()
        user_repo= UserRepositoryMock()
        usecase= UpdateWarningUsecase(repo=repo, user_repo=user_repo)
        controller= UpdateWarningController(usecase=usecase)

        request = HttpRequest(body={
            'user_from_authorizer':{
                'id': '550e8400-e29b-41d4-a716-446655440002',
                'displayName': 'Maria',
                'mail': '22.00678-2@maua.br',
            },
            'update_warning':{
                'warning_id': 'some-warning-id',
                'updated_warning':{
                    'title': 'Atualização de sistema - versão 2',
                    'description': 'O sistema será atualizado no próximo fim de semana. Esta é a versão 2.',
                },
            }
        })

        response= controller(request=request)
        assert response.status_code == 403
        assert response.body == 'Only ADM users can update warnings.'