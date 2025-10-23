from src.shared.domain.entities.user import User
from src.shared.domain.enums.active_enum import ACTIVE
from src.shared.domain.enums.course_enum import COURSE
from src.shared.domain.enums.organization_enum import ORGANIZATION
from src.shared.domain.enums.role_enum import ROLE
from src.shared.domain.enums.state_enum import STATE
from src.shared.helpers.errors.usecase_errors import ForbiddenAction, NoItemsFound
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock
import pytest
import uuid



class Test_UserRepositoryMock:
    def test_get_user(self):
        repo = UserRepositoryMock()
        user = repo.get_user(user_id="550e8400-e29b-41d4-a716-446655440000")

        assert user.name == "Guilherme"
        assert user.email == "25.00178-5@maua.br"
        assert user.user_id == "550e8400-e29b-41d4-a716-446655440000"
        assert user.state == STATE.PENDING
        assert user.role == ROLE.USER
        assert user.active == ACTIVE.ACTIVE


    def test_get_user_not_found(self):
        repo = UserRepositoryMock()
        with pytest.raises(NoItemsFound):
            user = repo.get_user(69)

    def test_get_all_user(self):
        repo = UserRepositoryMock()
        users = repo.get_all_user()
        assert len(users) == 8

    def test_create_user(self):
        repo = UserRepositoryMock()
        new_user = User(
            user_id=str(uuid.uuid4()),
            name="Vitor Soller",
            email="dohypevitin@maua.br",
            ra="20.00123-4",
            role=ROLE.USER,
            course=COURSE.ECM,
            year=5,
            organization=ORGANIZATION.DEV,
            state=STATE.PENDING,
            active=ACTIVE.ACTIVE
        )

        created_user = repo.create_user(new_user)

        assert created_user.name == "Vitor Soller"
        assert created_user.email == "dohypevitin@maua.br"
        assert created_user.ra == "20.00123-4"
        assert created_user.role == ROLE.USER
        assert created_user.course == COURSE.ECM
        assert created_user.year == 5
        assert created_user.organization == ORGANIZATION.DEV
        assert created_user.state == STATE.PENDING
        assert created_user.active == ACTIVE.ACTIVE

    def test_delete_user(self):
        repo = UserRepositoryMock()
        deleted_user = repo.delete_user(user_id="550e8400-e29b-41d4-a716-446655440000")
        assert deleted_user.name == "Guilherme"
        assert deleted_user.email == "25.00178-5@maua.br"
        assert deleted_user.user_id == "550e8400-e29b-41d4-a716-446655440000"
        assert deleted_user.state == STATE.PENDING
        assert deleted_user.role == ROLE.USER


    def test_delete_user_not_found(self):
        repo = UserRepositoryMock()
        with pytest.raises(NoItemsFound):
            deleted_user = repo.delete_user(user_id="550e8400-e29b-41d4-a716-446655440005")

    def test_update_user(self):
        repo = UserRepositoryMock()
        updated_user= repo.update_user(user_id="550e8400-e29b-41d4-a716-446655440000", new_state=STATE.APPROVED, new_role=ROLE.ADM, new_active=ACTIVE.ACTIVE, new_course=COURSE.EEN, new_year=4, new_organization=ORGANIZATION.NAWAT)

        assert updated_user.state == STATE.APPROVED
        assert updated_user.role == ROLE.ADM
        assert updated_user.course == COURSE.EEN
        assert updated_user.year == 4
        assert updated_user.organization == ORGANIZATION.NAWAT

        assert repo.users[0].state == STATE.APPROVED
        assert repo.users[0].role == ROLE.ADM
        assert repo.users[0].course == COURSE.EEN
        assert repo.users[0].year == 4
        assert repo.users[0].organization == ORGANIZATION.NAWAT

    def test_update_user_state_role_course_year_organization_are_none(self):
        repo = UserRepositoryMock()
        updated_user= repo.update_user(
            user_id="550e8400-e29b-41d4-a716-446655440001", 
            new_state=None, 
            new_role=None, 
            new_active=None, 
            new_course=None, 
            new_year=None, 
            new_organization=None
        )

        assert updated_user.state == STATE.APPROVED
        assert updated_user.role == ROLE.ADM
        assert updated_user.course == COURSE.CIC
        assert updated_user.active == ACTIVE.ACTIVE
        assert updated_user.year == 4
        assert updated_user.organization == ORGANIZATION.DEV

        assert repo.users[1].state == STATE.APPROVED
        assert repo.users[1].role == ROLE.ADM
        assert repo.users[1].active == ACTIVE.ACTIVE
        assert repo.users[1].course == COURSE.CIC
        assert repo.users[1].year == 4
        assert repo.users[1].organization == ORGANIZATION.DEV

    def test_update_user_not_found(self):
        repo = UserRepositoryMock()

        with pytest.raises(NoItemsFound):
            updated_user= repo.update_user(user_id="550e8400-e29b-41d4-a716-446655440005", new_state=STATE.APPROVED, new_role=ROLE.ADM, new_active=ACTIVE.ACTIVE, new_course=COURSE.CIC, new_year=4, new_organization=ORGANIZATION.DEV)

#     def test_get_users_counter(self):
#         repo = UserRepositoryMock()

#         assert repo.get_user_counter() == 3

    def test_has_permission_true(self):
        repo = UserRepositoryMock()
        new_user = User(
            user_id=str(uuid.uuid4()),
            name="Vitor Soller",
            email="20.00978-5@maua.br",
            ra="20.00978-5",
            role=ROLE.USER,
            course=COURSE.ECM,
            year=5,
            organization=ORGANIZATION.DEV,
            state=STATE.PENDING,
            active=ACTIVE.ACTIVE
        )
        id_user_requester= "e6bed58f-424a-4b62-b408-18e0a8d1f069"

        response= repo.has_permission_target_user(id_user_requester, new_user)

        assert response == True


    def test_has_permission_raise_forbidden(self):
        repo = UserRepositoryMock()
        new_user = User(
                    user_id=str(uuid.uuid4()),
                    name="Vitor Soller",
                    email="20.00123-4@maua.br",
                    ra="20.00123-4",
                    role=ROLE.USER,
                    course=COURSE.ECM,
                    year=5,
                    organization=ORGANIZATION.DEV,
                    state=STATE.PENDING,
                    active=ACTIVE.ACTIVE
        )
        id_user_requester= "550e8400-e29b-41d4-a716-446655440002"

        with pytest.raises(ForbiddenAction):
            repo.has_permission_target_user(id_user_requester, new_user)


    def test_has_permission_user_requester_does_not_has_the_same_organization_of_new_user(self):
        repo = UserRepositoryMock()
        new_user = User(
                    user_id=str(uuid.uuid4()),
                    name="Vitor Soller",
                    email="20.00123-4@maua.br",
                    ra="20.00123-4",
                    role=ROLE.USER,
                    course=COURSE.ECM,
                    year=5,
                    organization=ORGANIZATION.DEV,
                    state=STATE.PENDING,
                    active=ACTIVE.ACTIVE
        )
        id_user_requester= "550e8400-e29b-41d4-a716-446655440002"

        with pytest.raises(ForbiddenAction):
            response= repo.has_permission_target_user(id_user_requester, new_user)

    def test_has_permission_user_requester_not_found(self):
        repo = UserRepositoryMock()
        new_user = User(
                    user_id=str(uuid.uuid4()),
                    name="Vitor Soller",
                    email="20.00123-4@maua.br",
                    ra="20.00123-4",
                    role=ROLE.USER,
                    course=COURSE.ECM,
                    year=5,
                    organization=ORGANIZATION.DEV,
                    state=STATE.PENDING,
                    active=ACTIVE.ACTIVE
        )
        id_user_requester= "550e8400-e29b-41d4-a716-446655440005"

        with pytest.raises(NoItemsFound):
            repo.has_permission_target_user(id_user_requester, new_user)
            
            
    def test_has_permission_target_id_president_in_own_org(self):
        repo = UserRepositoryMock()
        target_user = User(
            user_id=str(uuid.uuid4()),
            name="Target User",
            email="23.00000-0@maua.br",
            ra="23.00000-0",
            role=ROLE.USER,
            organization=ORGANIZATION.DEV,
            active=ACTIVE.ACTIVE, course=COURSE.ECM, state=STATE.APPROVED, year=1
        )
        repo.create_user(target_user)
        
        dev_president_user = repo.get_dev_president()
        
        response = repo.has_permission_target_id(
            requester_id=dev_president_user.user_id,
            target_id=target_user.user_id
        )
        
        assert response == True
        
    def test_has_permission_target_id_common_user_raises_forbidden(self):
        repo = UserRepositoryMock()
        requester_user = User(
            user_id=str(uuid.uuid4()),
            name="Requester User",
            email="23.00001-0@maua.br",
            ra="23.00001-0",
            role=ROLE.USER,
            organization=ORGANIZATION.DEV,
            active=ACTIVE.ACTIVE, course=COURSE.ECM, state=STATE.APPROVED, year=1
        )
        repo.create_user(requester_user)
        
        dev_president_user = repo.get_dev_president()
        
        with pytest.raises(ForbiddenAction) as e:
            repo.has_permission_target_id(
                requester_id=requester_user.user_id,
                target_id=dev_president_user.user_id
            )
        assert e.value.message == "Common user is not allowed to perform actions in other entities"

    def test_has_permission_target_id_president_outside_org_raises_forbidden(self):
        repo = UserRepositoryMock()
        target_user = User(
            user_id=str(uuid.uuid4()),
            name="Target User",
            email="23.00000-0@maua.br",
            ra="23.00000-0",
            role=ROLE.USER,
            organization=ORGANIZATION.DEV,
            active=ACTIVE.ACTIVE, course=COURSE.ECM, state=STATE.APPROVED, year=1
        )
        repo.create_user(target_user)
        
        nawat_president_user = repo.get_nawat_president()
        
        with pytest.raises(ForbiddenAction) as e:
            repo.has_permission_target_id(
                requester_id=nawat_president_user.user_id,
                target_id=target_user.user_id
            )
        assert e.value.message == "President is not allowed to perform action in other organization besides he's"

    def test_has_permission_target_id_admin_on_any_user(self):
        repo = UserRepositoryMock()
        target_user = User(
            user_id=str(uuid.uuid4()),
            name="Target User",
            email="23.00000-0@maua.br",
            ra="23.00000-0",
            role=ROLE.USER,
            organization=ORGANIZATION.DEV,
            active=ACTIVE.ACTIVE, course=COURSE.ECM, state=STATE.APPROVED, year=1
        )
        repo.create_user(target_user)
        
        system_admin = repo.get_system_admin()
        nawat_president_user = repo.get_nawat_president()
        
        # Admin on president
        response_admin_on_president = repo.has_permission_target_id(
            requester_id=system_admin.user_id,
            target_id=nawat_president_user.user_id
        )
        assert response_admin_on_president == True
        
        # Admin on common user
        response_admin_on_user = repo.has_permission_target_id(
            requester_id=system_admin.user_id,
            target_id=target_user.user_id
        )
        assert response_admin_on_user == True
            
    def test_get_users(self):
        repo = UserRepositoryMock()
        users = repo.get_users()
        assert len(users) == 8

    def test_get_users_approved_from_dev(self):
        repo = UserRepositoryMock()
        users = repo.get_users(organization=ORGANIZATION.DEV, state=STATE.APPROVED)
        assert len(users) == 3
        for user in users:
            assert user.organization == ORGANIZATION.DEV
            assert user.state == STATE.APPROVED

    def test_get_users_pending_from_nawat(self):
        repo = UserRepositoryMock()
        users = repo.get_users(organization=ORGANIZATION.NAWAT, state=STATE.PENDING)
        assert len(users) == 1
        for user in users:
            assert user.organization == ORGANIZATION.NAWAT
            assert user.state == STATE.PENDING

    def test_get_users_cic_course(self):
        repo = UserRepositoryMock()
        users = repo.get_users(course = COURSE.CIC)
        assert len(users) == 1
        for user in users:
            assert user.course == COURSE.CIC

    def test_get_users_fourth_grade(self):
        repo = UserRepositoryMock()
        users = repo.get_users(year = 4)
        assert len(users) == 3
        for user in users:
            assert user.year == 4