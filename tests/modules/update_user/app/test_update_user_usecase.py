import pytest

from src.modules.update_user.app.update_user_usecase import UpdateUserUsecase
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import NoItemsFound
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock
from src.shared.domain.enums.course_enum import COURSE
from src.shared.domain.enums.organization_enum import ORGANIZATION
from src.shared.domain.enums.role_enum import ROLE
from src.shared.domain.enums.state_enum import STATE

class Test_UpdateUserUsecase:
    def test_update_user_usecase(selfs):
        repo = UserRepositoryMock()
        usecase = UpdateUserUsecase(repo=repo)
        updated_user = usecase(name="Heitor", user_id="550e8400-e29b-41d4-a716-446655440002", email="23.00768-0", ra="23.00768-0", new_state=STATE.APPROVED, new_role=ROLE.USER, new_course=COURSE.CIC, new_year=4, new_organization=ORGANIZATION.DEV)

        assert updated_user.name == "Heitor"

    def test_update_user_usecase_wrong_user_id(selfs):
        repo = UserRepositoryMock()
        usecase = UpdateUserUsecase(repo=repo)

        with pytest.raises(EntityError):
            usecase(user_id="550e8400-e29b-41d4-a716-44665544000", name="Heitor", email="23.00768-0", ra="23.00768-0", new_state=STATE.APPROVED, new_role=ROLE.USER, new_course=COURSE.CIC, new_year=4, new_organization=ORGANIZATION.DEV)

    def test_update_user_usecase_wrong_new_name(selfs):
        repo = UserRepositoryMock()
        usecase = UpdateUserUsecase(repo=repo)

        with pytest.raises(EntityError):
            usecase(user_id="550e8400-e29b-41d4-a716-44665544000", name=1, email="23.00768-0", ra="23.00768-0", new_state=STATE.APPROVED, new_role=ROLE.USER,new_course=COURSE.CIC, new_year=4, new_organization=ORGANIZATION.DEV)

    def test_update_user_usecase_wrong_new_email(selfs):
        repo = UserRepositoryMock()
        usecase = UpdateUserUsecase(repo=repo)

        with pytest.raises(EntityError):
            usecase(user_id="550e8400-e29b-41d4-a716-44665544000", name="Heitor", email=1, ra="23.00768-0", new_state=STATE.APPROVED, new_role=ROLE.USER,new_course=COURSE.CIC, new_year=4, new_organization=ORGANIZATION.DEV)

    def test_update_user_usecase_wrong_new_ra(selfs):
        repo = UserRepositoryMock()
        usecase = UpdateUserUsecase(repo=repo)

        with pytest.raises(EntityError):
            usecase(user_id="550e8400-e29b-41d4-a716-44665544000", name="Heitor", email="23.00768-0", ra=1, new_state=STATE.APPROVED, new_role=ROLE.USER,new_course=COURSE.CIC, new_year=4, new_organization=ORGANIZATION.DEV)

    def test_update_user_usecase_wrong_new_state(selfs):
        repo = UserRepositoryMock()
        usecase = UpdateUserUsecase(repo=repo)

        with pytest.raises(EntityError):
            usecase(user_id="550e8400-e29b-41d4-a716-44665544000", name="Heitor", email="23.00768-0", ra="23.00768-0", new_state="APPROVED", new_role=ROLE.USER,new_course=COURSE.CIC, new_year=4, new_organization=ORGANIZATION.DEV)

    def test_update_user_usecase_wrong_new_role(selfs):
        repo = UserRepositoryMock()
        usecase = UpdateUserUsecase(repo=repo)

        with pytest.raises(EntityError):
            usecase(user_id="550e8400-e29b-41d4-a716-44665544000", name="Heitor", email="23.00768-0", ra="23.00768-0", new_state=STATE.APPROVED, new_role="USER",new_course=COURSE.CIC, new_year=4, new_organization=ORGANIZATION.DEV)

    def test_update_user_usecase_wrong_new_course(selfs):
        repo = UserRepositoryMock()
        usecase = UpdateUserUsecase(repo=repo)

        with pytest.raises(EntityError):
            usecase(user_id="550e8400-e29b-41d4-a716-44665544000", name="Heitor", email="23.00768-0", ra="23.00768-0", new_state=STATE.APPROVED, new_role=ROLE.USER,new_course="CIC", new_year=4, new_organization=ORGANIZATION.DEV)

    def test_update_user_usecase_wrong_new_year(selfs):
        repo = UserRepositoryMock()
        usecase = UpdateUserUsecase(repo=repo)

        with pytest.raises(EntityError):
            usecase(user_id="550e8400-e29b-41d4-a716-44665544000", name="Heitor", email="23.00768-0", ra="23.00768-0", new_state=STATE.APPROVED, new_role=ROLE.USER,new_course=COURSE.CIC, new_year="4", new_organization=ORGANIZATION.DEV)

    def test_update_user_usecase_wrong_new_organization(selfs):
        repo = UserRepositoryMock()
        usecase = UpdateUserUsecase(repo=repo)

        with pytest.raises(EntityError):
            usecase(user_id="550e8400-e29b-41d4-a716-44665544000", name="Heitor", email="23.00768-0", ra="23.00768-0", new_state=STATE.APPROVED, new_role=ROLE.USER,new_course=COURSE.CIC, new_year=4, new_organization="DEV")

    def test_update_user_usecase_user_not_found(selfs):
        repo = UserRepositoryMock()
        usecase = UpdateUserUsecase(repo=repo)

        with pytest.raises(NoItemsFound):
            usecase(user_id="550e8400-e29b-41d4-a716-446655440009", name="Heitor", email="23.00768-0", ra="23.00768-0", new_state=STATE.APPROVED, new_role=ROLE.USER,new_course=COURSE.CIC, new_year=4, new_organization=ORGANIZATION.DEV)

    