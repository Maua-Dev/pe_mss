import pytest
from src.modules.get_all_users.app.get_all_users_usecase import GetAllUsersUsecase
from src.shared.domain.entities.user import User
from src.shared.domain.enums.organization_enum import ORGANIZATION
from src.shared.domain.enums.state_enum import STATE
from src.shared.helpers.errors.usecase_errors import ForbiddenAction, NoItemsFound
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock

class Test_GetAllUsersUsecase:
    def test_get_all_users_usecase(self):
        userrepo = UserRepositoryMock()
        usecase = GetAllUsersUsecase(userrepo=userrepo)

        users = usecase("550e8400-e29b-41d4-a716-446655440001")
        assert type(users) == list
        assert len(users) == 8
        assert all([type(user) == User for user in users])


    def test_get_all_users_from_dev(self):
        userrepo = UserRepositoryMock()
        usecase = GetAllUsersUsecase(userrepo=userrepo)

        users = usecase("550e8400-e29b-41d4-a716-446655440001", organization=ORGANIZATION.DEV)
        assert type(users) == list
        assert len(users) == 4
        assert all([type(user) == User for user in users])
        assert all([user.organization == ORGANIZATION.DEV for user in users])

    def test_get_all_users_from_nawat(self):
        userrepo = UserRepositoryMock()
        usecase = GetAllUsersUsecase(userrepo=userrepo)

        users = usecase("550e8400-e29b-41d4-a716-446655440001", organization=ORGANIZATION.NAWAT)
        assert type(users) == list
        assert len(users) == 2
        assert all([type(user) == User for user in users])
        assert all([user.organization == ORGANIZATION.NAWAT for user in users])

    def test_get_all_users_approved(self):
        userrepo = UserRepositoryMock()
        usecase = GetAllUsersUsecase(userrepo=userrepo)

        users = usecase("550e8400-e29b-41d4-a716-446655440001", state=STATE.APPROVED)
        assert type(users) == list
        assert len(users) == 4
        assert all([type(user) == User for user in users])
        assert all([user.state == STATE.APPROVED for user in users])

    def test_get_all_users_approved_from_dev(self):
        userrepo = UserRepositoryMock()
        usecase = GetAllUsersUsecase(userrepo=userrepo)

        users = usecase("550e8400-e29b-41d4-a716-446655440001", organization=ORGANIZATION.DEV, state=STATE.APPROVED)
        assert type(users) == list
        assert len(users) == 3
        assert all([type(user) == User for user in users])
        assert all([user.organization == ORGANIZATION.DEV for user in users])
        assert all([user.state == STATE.APPROVED for user in users])

    def test_get_all_users_id_not_found(self):
        userrepo = UserRepositoryMock()
        usecase = GetAllUsersUsecase(userrepo=userrepo)

        with pytest.raises(NoItemsFound):
            users = usecase(user_id="xxxxxxxx-xxxx-xxxx-xxxx-xxxxxdxxxxxx")

    def test_get_all_users_inactive_user(self):
        userrepo = UserRepositoryMock()
        usecase = GetAllUsersUsecase(userrepo=userrepo)

        with pytest.raises(ForbiddenAction):
            users = usecase(user_id="3d32ec27-09c3-41da-92e2-be106e449b6a")