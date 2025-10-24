import pytest
from src.modules.update_user.app.update_user_controller import UpdateUserController
from src.modules.update_user.app.update_user_usecase import UpdateUserUsecase
from src.shared.domain.enums.course_enum import COURSE
from src.shared.domain.enums.organization_enum import ORGANIZATION
from src.shared.domain.enums.role_enum import ROLE
from src.shared.domain.enums.state_enum import STATE
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.external_interfaces.http_models import HttpRequest
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock
from src.shared.domain.enums.active_enum import ACTIVE

class Test_UpdateUserController:
    def test_update_user_controller(self):
        repo = UserRepositoryMock()
        usecase = UpdateUserUsecase(repo=repo)
        controller = UpdateUserController(usecase=usecase)

        request = HttpRequest(body={
            'user_id': repo.users[0].user_id,
            'new_state': STATE.APPROVED,
            'new_role': ROLE.USER,
            'new_course': COURSE.ARQ,   # opcional
            'new_year': 3,          # opcional
            'new_active': ACTIVE.ACTIVE  # opcional
        })

        response = controller(request=request)

        assert response.status_code == 200
        assert response.body['course'].name == 'ARQ'
        assert response.body['year'] == 3

    def test_update_user_with_organization(self):
        repo = UserRepositoryMock()
        usecase = UpdateUserUsecase(repo=repo)
        controller = UpdateUserController(usecase=usecase)

        request = HttpRequest(body={
            'user_id': repo.users[1].user_id,
            'new_state': STATE.APPROVED,
            'new_role': ROLE.USER,
            'new_organization': ORGANIZATION.DEV,  # opcional
            'new_course': COURSE.CIC,
            'new_year': repo.users[1].year
            
        })

        response = controller(request=request)

        assert response.status_code == 200
        assert response.body['organization'].name == 'DEV'
        assert response.body['year'] == repo.users[1].year


    def test_update_user_invalid_course_enum(self):
        repo = UserRepositoryMock()
        usecase = UpdateUserUsecase(repo=repo)

        with pytest.raises(EntityError, match="course"):
            usecase(
                new_state=STATE.APPROVED,
                new_role=ROLE.PRESIDENT,
                new_course="INVALIDO",  # erro aqui
                user_id=repo.users[2].user_id
            )

    def test_update_user_controller_invalid_user_id(self):
        repo = UserRepositoryMock()
        usecase = UpdateUserUsecase(repo=repo)
        controller = UpdateUserController(usecase=usecase)

        request = HttpRequest(body={
            'user_id': repo.users[2].user_id,
            'new_state': STATE.APPROVED,
            'new_role': ROLE.PRESIDENT,
            'new_year': "terceiro"  # errado, deveria ser int
        })

        response = controller(request=request)

        assert response.status_code == 400
        assert "Field new_year isn't in the right type" in response.body
