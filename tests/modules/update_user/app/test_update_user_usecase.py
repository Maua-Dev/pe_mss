# import pytest

import pytest
from src.modules.update_user.app.update_user_usecase import UpdateUserUsecase
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import ForbiddenAction, NoItemsFound
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
            requester_id="550e8400-e29b-41d4-a716-446655440001",
            target_id="550e8400-e29b-41d4-a716-446655440002",
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
                requester_id="550e8400-e29b-41d4-a716-446655440001",
                target_id="550e8400-e29b-41d4-a716-44665544000",  # inválido
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
                requester_id="550e8400-e29b-41d4-a716-446655440001",
                target_id="550e8400-e29b-41d4-a716-446655440002",
                new_state=5,  
                new_role=ROLE.USER.value,
                new_course=COURSE.CIC.value,
                new_year=4,
                new_organization=ORGANIZATION.DEV.value
            )

    def test_update_user_usecase_wrong_new_role(self):
        repo = UserRepositoryMock()
        usecase = UpdateUserUsecase(repo=repo)
        with pytest.raises(EntityError):
            usecase(
                requester_id="550e8400-e29b-41d4-a716-446655440001",
                target_id="550e8400-e29b-41d4-a716-446655440002",
                new_state=STATE.APPROVED,
                new_role="adm", # string inválida, deve ser ROLE  
                new_course=COURSE.CIC,
                new_year=4,
                new_organization=ORGANIZATION.DEV
            )

    def test_update_user_usecase_wrong_new_course(self):
        repo = UserRepositoryMock()
        usecase = UpdateUserUsecase(repo=repo)
        with pytest.raises(EntityError):
            usecase(
                requester_id="550e8400-e29b-41d4-a716-446655440001",
                target_id="550e8400-e29b-41d4-a716-446655440002",
                new_state=STATE.APPROVED,
                new_role=ROLE.USER,
                new_course="ola",  # string inválida, deve ser COURSE
                new_year=4,
                new_organization=ORGANIZATION.DEV
            )

    def test_update_user_usecase_wrong_new_year(self):
        repo = UserRepositoryMock()
        usecase = UpdateUserUsecase(repo=repo)
        with pytest.raises(EntityError):
            usecase(
                requester_id="550e8400-e29b-41d4-a716-446655440001",
                target_id="550e8400-e29b-41d4-a716-446655440002",
                new_state=STATE.APPROVED,
                new_role=ROLE.USER,
                new_course=COURSE.CIC,
                new_year="Ola" ,  # string inválida, deve ser int
                new_organization=ORGANIZATION.DEV
            )

    def test_update_user_usecase_wrong_new_organization(self):
        repo = UserRepositoryMock()
        usecase = UpdateUserUsecase(repo=repo)
        with pytest.raises(EntityError):
            usecase(
                requester_id="550e8400-e29b-41d4-a716-446655440001",
                target_id="550e8400-e29b-41d4-a716-446655440002",
                new_state=STATE.APPROVED,
                new_role=ROLE.USER,
                new_course=COURSE.CIC,
                new_year=4,
                new_organization="5"  # string inválida, deve ser ORGANIZATION
            )

    def test_update_user_usecase_user_not_found(self):
        repo = UserRepositoryMock()
        usecase = UpdateUserUsecase(repo=repo)
        with pytest.raises(NoItemsFound):
            usecase(
                requester_id="550e8400-e29b-41d4-a716-446655440001",
                target_id="550e8400-e29b-41d4-a716-446655440009",  # não existe
                new_state=STATE.APPROVED,
                new_role=ROLE.USER,
                new_course=COURSE.CIC,
                new_year=4,
                new_organization=ORGANIZATION.DEV
            )
            
    def test_president_cannot_rebaixar_adm(self):
        repo = UserRepositoryMock()
        usecase = UpdateUserUsecase(repo=repo)

        with pytest.raises(ForbiddenAction):
            usecase(
                requester_id="550e8400-e29b-41d4-a716-446655440002",  # PRESIDENT
                target_id="550e8400-e29b-41d4-a716-446655440001",    # ADM
                new_role=ROLE.USER                                   # tentativa de rebaixar
            )

    def test_president_cannot_promote_user_to_adm(self):
        repo = UserRepositoryMock()
        usecase = UpdateUserUsecase(repo=repo)

        with pytest.raises(ForbiddenAction):
            usecase(
                requester_id="550e8400-e29b-41d4-a716-446655440002",  # PRESIDENT
                target_id="550e8400-e29b-41d4-a716-446655440000",    # USER
                new_role=ROLE.ADM                                     # tentativa de promover
            )

    def test_non_adm_cannot_transfer_organization(self):
        repo = UserRepositoryMock()
        usecase = UpdateUserUsecase(repo=repo)

        with pytest.raises(ForbiddenAction):
            usecase(
                requester_id="550e8400-e29b-41d4-a716-446655440002",  # PRESIDENT
                target_id="550e8400-e29b-41d4-a716-446655440000",    # USER
                new_organization=ORGANIZATION.DEV                     # presidente não pode trocar org
            )

    def test_user_cannot_change_own_role(self):
        repo = UserRepositoryMock()
        usecase = UpdateUserUsecase(repo=repo)

        with pytest.raises(ForbiddenAction):
            usecase(
                requester_id="550e8400-e29b-41d4-a716-446655440000",  # USER
                target_id="550e8400-e29b-41d4-a716-446655440000",    # ele mesmo
                new_role=ROLE.ADM                                     # tentanto se promover
            )
