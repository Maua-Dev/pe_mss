import datetime
from src.modules.create_warning.app.create_warning_controller import CreateWarningController
from src.modules.create_warning.app.create_warning_usecase import CreateWarningUsecase
from src.shared.helpers.external_interfaces.http_models import HttpRequest
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock
from src.shared.infra.repositories.warning_repository_mock import WarningRepositoryMock


class Test_CreateWarningController:
    def test_create_warning_controller_without_user_from_authorizer(self):
        repo = WarningRepositoryMock()
        user_repo= UserRepositoryMock()
        usecase= CreateWarningUsecase(repo=repo, user_repo=user_repo)
        controller= CreateWarningController(usecase=usecase)

        request = HttpRequest()

        response = controller(request=request)

        assert response.status_code == 400
        assert response.body == 'Field user_from_authorizer is missing'

    def test_create_warning_controller_without_new_warning(self):
        repo = WarningRepositoryMock()
        user_repo= UserRepositoryMock()
        usecase= CreateWarningUsecase(repo=repo, user_repo=user_repo)
        controller= CreateWarningController(usecase=usecase)

        request = HttpRequest(body={
            'user_from_authorizer':{
                'id': '550e8400-e29b-41d4-a716-446655440001',
                'displayName': 'João',
                'mail': '21.00678-2@maua.br'
            },
        })

        response= controller(request=request)

        assert response.status_code == 400
        assert response.body == 'Field new_warning is missing'
    
    def test_create_warning_controller_with_specif_warning_and_as_admin(self):
        repo = WarningRepositoryMock()
        user_repo= UserRepositoryMock()
        usecase= CreateWarningUsecase(repo=repo, user_repo=user_repo)
        controller= CreateWarningController(usecase=usecase)

        request = HttpRequest(body={
            'user_from_authorizer':{
                'id': '550e8400-e29b-41d4-a716-446655440001',
                'displayName': 'João',
                'mail': '21.00678-2@maua.br'
            },
            'new_warning':{
                'title': 'Manutenção no sistema',
                'description': 'O sistema ficará indisponível para manutenção.',
                'expire': '2025-12-31T23:59:59',
                'target_role': 'PRESIDENT',
                'target_org': 'DEV'
            }
        })

        response= controller(request=request)

        assert response.status_code == 200
        assert response.body["warning"]['warning_id'] is not None
        assert response.body["warning"]['body']['title'] == 'Manutenção no sistema'
        assert response.body["warning"]['body']['description'] == 'O sistema ficará indisponível para manutenção.'
        assert response.body["warning"]['body']['expire'] == datetime.datetime(2025, 12, 31, 23, 59, 59)
        assert response.body["warning"]['target_role'] == 'PRESIDENT'
        assert response.body["warning"]['target_org'] == 'DEV'

    def test_create_warning_controller_with_general_warning_and_as_adm(self):
        repo = WarningRepositoryMock()
        user_repo= UserRepositoryMock()
        usecase= CreateWarningUsecase(repo=repo, user_repo=user_repo)
        controller= CreateWarningController(usecase=usecase)

        request = HttpRequest(body={
            'user_from_authorizer':{
                'id': '550e8400-e29b-41d4-a716-446655440001',
                'displayName': 'João',
                'mail': '21.00678-2@maua.br'
            },
            'new_warning':{
                'title': 'Atualização de política',
                'description': 'Haverá uma atualização na política de uso.',
                'expire': '2025-11-30T23:59:59',
                'target_role': 'USER',
                # No target_org is provided for general warning
            }
        })

        response= controller(request=request)

        assert response.status_code == 200
        assert response.body["warning"]['warning_id'] is not None
        assert response.body["warning"]['body']['title'] == 'Atualização de política'
        assert response.body["warning"]['body']['description'] == 'Haverá uma atualização na política de uso.'
        assert response.body["warning"]['body']['expire'] == datetime.datetime(2025, 11, 30, 23, 59, 59)
        assert response.body["warning"]['target_role'] == 'USER'
        assert response.body["warning"]['target_org'] is None

    # in this first version, only ADM users can create warnings, PRESIDENT and USER can't
    def test_create_warning_controller_as_non_admin(self):
        repo = WarningRepositoryMock()
        user_repo= UserRepositoryMock()
        usecase= CreateWarningUsecase(repo=repo, user_repo=user_repo)
        controller= CreateWarningController(usecase=usecase)

        # the test is beeing done with a USER in case that in future we allow PRESIDENT users to create warnings
        request = HttpRequest(body={
            'user_from_authorizer':{
                'id': '550e8400-e29b-41d4-a716-446655440000',
                'displayName': 'Guilherme',
                'mail': '25.00178-5@maua.br'
            },
            'new_warning':{
                'title': 'Manutenção no sistema',
                'description': 'O sistema ficará indisponível para manutenção.',
                'expire': '2025-12-31T23:59:59',
                'target_role': 'PRESIDENT',
                'target_org': 'DEV'
            }
        }) 

        response= controller(request=request)

        assert response.status_code == 403
        assert response.body == 'Only ADM users can create warnings.'

    def test_create_warning_controller_with_past_expire_date(self):
        repo = WarningRepositoryMock()
        user_repo= UserRepositoryMock()
        usecase= CreateWarningUsecase(repo=repo, user_repo=user_repo)
        controller= CreateWarningController(usecase=usecase)

        request = HttpRequest(body={
            'user_from_authorizer':{
                'id': '550e8400-e29b-41d4-a716-446655440001',
                'displayName': 'João',
                'mail': '21.00678-2@maua.br'
            },
            'new_warning':{
                'title': 'Manutenção no sistema',
                'description': 'O sistema ficará indisponível para manutenção.',
                'expire': '2022-12-31T23:59:59',
                'target_role': 'PRESIDENT',
                'target_org': 'DEV'
            }
        })

        response= controller(request=request)

        assert response.status_code == 400
        assert response.body == 'Field expire isn\'t in the right type.\n Received: 2022-12-31T23:59:59.\n Expected: a future date'