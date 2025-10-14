# import pytest

from src.modules.update_user.app.update_user_usecase import UpdateUserUsecase
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import NoItemsFound
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock
from src.shared.domain.enums.course_enum import COURSE
from src.shared.domain.enums.organization_enum import ORGANIZATION
from src.shared.domain.enums.role_enum import ROLE
from src.shared.domain.enums.state_enum import STATE

class Test_UpdateUserUsecase:

    def test_update_user_usecase(self):
        repo = UserRepositoryMock()
        usecase = UpdateUserUsecase(repo=repo)
        updated_user = usecase(
            user_id="550e8400-e29b-41d4-a716-446655440002",
            new_state=STATE.APPROVED,
            new_role=ROLE.USER,
            new_course=COURSE.CIC,
            new_year=4,
            new_organization=ORGANIZATION.DEV
        )
        assert updated_user.user_id == "550e8400-e29b-41d4-a716-446655440002"

    def test_update_user_usecase_wrong_user_id(self):
        repo = UserRepositoryMock()
        usecase = UpdateUserUsecase(repo=repo)
        with pytest.raises(EntityError):
            usecase(
                user_id="550e8400-e29b-41d4-a716-44665544000",  # inválido
                new_state=STATE.APPROVED,
                new_role=ROLE.USER,
                new_course=COURSE.CIC,
                new_year=4,
                new_organization=ORGANIZATION.DEV
            )

    def test_update_user_usecase_wrong_new_state(self):
        repo = UserRepositoryMock()
        usecase = UpdateUserUsecase(repo=repo)
        with pytest.raises(EntityError):
            usecase(
                user_id="550e8400-e29b-41d4-a716-446655440002",
                new_state="APPROVED",  # string inválida, deve ser STATE
                new_role=ROLE.USER,
                new_course=COURSE.CIC,
                new_year=4,
                new_organization=ORGANIZATION.DEV
            )

    def test_update_user_usecase_wrong_new_role(self):
        repo = UserRepositoryMock()
        usecase = UpdateUserUsecase(repo=repo)
        with pytest.raises(EntityError):
            usecase(
                user_id="550e8400-e29b-41d4-a716-446655440002",
                new_state=STATE.APPROVED,
                new_role="USER",  # string inválida, deve ser ROLE
                new_course=COURSE.CIC,
                new_year=4,
                new_organization=ORGANIZATION.DEV
            )

    def test_update_user_usecase_wrong_new_course(self):
        repo = UserRepositoryMock()
        usecase = UpdateUserUsecase(repo=repo)
        with pytest.raises(EntityError):
            usecase(
                user_id="550e8400-e29b-41d4-a716-446655440002",
                new_state=STATE.APPROVED,
                new_role=ROLE.USER,
                new_course="CIC",  # string inválida, deve ser COURSE
                new_year=4,
                new_organization=ORGANIZATION.DEV
            )

    def test_update_user_usecase_wrong_new_year(self):
        repo = UserRepositoryMock()
        usecase = UpdateUserUsecase(repo=repo)
        with pytest.raises(EntityError):
            usecase(
                user_id="550e8400-e29b-41d4-a716-446655440002",
                new_state=STATE.APPROVED,
                new_role=ROLE.USER,
                new_course=COURSE.CIC,
                new_year="4",  # string inválida, deve ser int
                new_organization=ORGANIZATION.DEV
            )

    def test_update_user_usecase_wrong_new_organization(self):
        repo = UserRepositoryMock()
        usecase = UpdateUserUsecase(repo=repo)
        with pytest.raises(EntityError):
            usecase(
                user_id="550e8400-e29b-41d4-a716-446655440002",
                new_state=STATE.APPROVED,
                new_role=ROLE.USER,
                new_course=COURSE.CIC,
                new_year=4,
                new_organization="DEV"  # string inválida, deve ser ORGANIZATION
            )

    def test_update_user_usecase_user_not_found(self):
        repo = UserRepositoryMock()
        usecase = UpdateUserUsecase(repo=repo)
        with pytest.raises(NoItemsFound):
            usecase(
                user_id="550e8400-e29b-41d4-a716-446655440009",  # não existe
                new_state=STATE.APPROVED,
                new_role=ROLE.USER,
                new_course=COURSE.CIC,
                new_year=4,
                new_organization=ORGANIZATION.DEV
            )
