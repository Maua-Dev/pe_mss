from src.shared.domain.enums.course_enum import COURSE
from src.shared.domain.enums.organization_enum import ORGANIZATION
from src.shared.domain.enums.role_enum import ROLE
from src.shared.domain.enums.state_enum import STATE
from src.shared.helpers.errors.usecase_errors import NoItemsFound
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock
import pytest




class Test_UserRepositoryMock:
#     def test_get_user(self):
#         repo = UserRepositoryMock()
#         deleted_user = repo.get_user(1)

#         assert deleted_user.name == "Bruno Soller"
#         assert deleted_user.email == "soller@soller.com"
#         assert deleted_user.user_id == 1
#         assert deleted_user.state == STATE.APPROVED

#     def test_get_user_not_found(self):
#         repo = UserRepositoryMock()
#         with pytest.raises(NoItemsFound):
#             deleted_user = repo.get_user(69)

#     def test_get_all_user(self):
#         repo = UserRepositoryMock()
#         users = repo.get_all_user()
#         assert len(users) == 3

#     def test_create_user(self):
#         repo = UserRepositoryMock()
#         deleted_user = User(
#             name="Vitor Soller",
#             email="dohype@vitin.com",
#             user_id=4,
#             state=STATE.PENDING
#         )

#         repo.create_user(deleted_user)

#         assert repo.users[3].name == "Vitor Soller"
#         assert repo.users[3].email == "dohype@vitin.com"
#         assert repo.users[3].user_id == 4
#         assert repo.users[3].state == STATE.PENDING

#         assert repo.user_counter == 4

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
        updated_user= repo.update_user(user_id="550e8400-e29b-41d4-a716-446655440000", new_state=STATE.APPROVED, new_role=ROLE.ADM, new_course=COURSE.EEN, new_year=4, new_organization=ORGANIZATION.DEV)
        
        assert updated_user.state == STATE.APPROVED
        assert updated_user.role == ROLE.ADM
        assert updated_user.course == COURSE.EEN
        assert updated_user.year == 4
        assert updated_user.organization == ORGANIZATION.DEV

        assert repo.users[0].state == STATE.APPROVED
        assert repo.users[0].role == ROLE.ADM
        assert repo.users[0].course == COURSE.EEN
        assert repo.users[0].year == 4
        assert repo.users[0].organization == ORGANIZATION.DEV

    def test_update_user_state_role_course_year_organization_are_none(self):
        repo = UserRepositoryMock()
        updated_user= repo.update_user(user_id="550e8400-e29b-41d4-a716-446655440001", new_state=None, new_role=None, new_course=None, new_year=None, new_organization=None)

        assert updated_user.state == STATE.APPROVED
        assert updated_user.role == ROLE.ADM
        assert updated_user.course == COURSE.CIC
        assert updated_user.year == 4
        assert updated_user.organization == ORGANIZATION.DEV

        assert repo.users[1].state == STATE.APPROVED
        assert repo.users[1].role == ROLE.ADM
        assert repo.users[1].course == COURSE.CIC
        assert repo.users[1].year == 4
        assert repo.users[1].organization == ORGANIZATION.DEV

    def test_update_user_not_found(self):
        repo = UserRepositoryMock()

        with pytest.raises(NoItemsFound):
            updated_user= repo.update_user(user_id="550e8400-e29b-41d4-a716-446655440005", new_state=STATE.APPROVED, new_role=ROLE.ADM, new_course=COURSE.CIC, new_year=4, new_organization=ORGANIZATION.DEV)

#     def test_get_users_counter(self):
#         repo = UserRepositoryMock()

#         assert repo.get_user_counter() == 3

