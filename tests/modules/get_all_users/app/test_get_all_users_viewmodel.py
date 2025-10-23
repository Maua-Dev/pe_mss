from src.modules.get_all_users.app.get_all_users_usecase import GetAllUsersUsecase
from src.modules.get_all_users.app.get_all_users_viewmodel import GetAllUsersViewModel
from src.shared.domain.enums.organization_enum import ORGANIZATION
from src.shared.domain.enums.state_enum import STATE
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock


class Test_GetAllUsersViewmodel:

    def test_get_all_users_viewmodel(self):
        userrepo = UserRepositoryMock()
        usecase = GetAllUsersUsecase(userrepo=userrepo)
        users = usecase(user_id="550e8400-e29b-41d4-a716-446655440001")

        viewmodel = GetAllUsersViewModel(users=users).to_dict()
        expected = {
            'users': [
                {
                    'user_id': u.user_id,
                    'name': u.name,
                    'email': u.email,
                    'state': (u.state.value if u.state is not None else None),
                    'role': (u.role.value if u.role is not None else None),
                    'active': (u.active.value if u.active is not None else None),
                    'ra': u.ra,
                    'course': (u.course.value if u.course is not None else None),
                    'year': u.year,
                    'organization': (u.organization.value if u.organization is not None else None),
                } for u in sorted(users, key=lambda x: x.name.casefold())
            ],
            'message': 'the users were retrieved'
        }

        assert viewmodel == expected

    def test_get_all_users_vewmodel_from_dev(self):
        userrepo = UserRepositoryMock()
        usecase = GetAllUsersUsecase(userrepo=userrepo)

        users = usecase(user_id="550e8400-e29b-41d4-a716-446655440002", organization=ORGANIZATION.DEV)

        viewmodel = GetAllUsersViewModel(users=users).to_dict()
        expected = {
            'users': [
                {
                    'user_id': u.user_id,
                    'name': u.name,
                    'email': u.email,
                    'state': (u.state.value if u.state is not None else None),
                    'role': (u.role.value if u.role is not None else None),
                    'active': (u.active.value if u.active is not None else None),
                    'ra': u.ra,
                    'course': (u.course.value if u.course is not None else None),
                    'year': u.year,
                    'organization': (u.organization.value if u.organization is not None else None),
                } for u in sorted(users, key=lambda x: x.name.casefold())
            ],
            'message': 'the users were retrieved'
        }

        assert viewmodel == expected

    def test_get_all_users_viewmodel_approved_state(self):
        userrepo = UserRepositoryMock()
        usecase = GetAllUsersUsecase(userrepo=userrepo)

        users = usecase(user_id="550e8400-e29b-41d4-a716-446655440001", state=STATE.APPROVED)

        viewmodel = GetAllUsersViewModel(users=users).to_dict()
        expected = {
            'users': [
                {
                    'user_id': u.user_id,
                    'name': u.name,
                    'email': u.email,
                    'state': (u.state.value if u.state is not None else None),
                    'role': (u.role.value if u.role is not None else None),
                    'active': (u.active.value if u.active is not None else None),
                    'ra': u.ra,
                    'course': (u.course.value if u.course is not None else None),
                    'year': u.year,
                    'organization': (u.organization.value if u.organization is not None else None),
                } for u in sorted(users, key=lambda x: x.name.casefold())
            ],
            'message': 'the users were retrieved'
        }

        assert viewmodel == expected

    def test_get_all_users_viewmodel_nawat_approved(self):
        userrepo = UserRepositoryMock()
        usecase = GetAllUsersUsecase(userrepo=userrepo)

        users = usecase(
            user_id="b423780f-2045-44e1-9c0b-98352841817d",
            organization=ORGANIZATION.NAWAT,
            state=STATE.APPROVED
        )

        viewmodel = GetAllUsersViewModel(users=users).to_dict()
        expected = {
            'users': [
                {
                    'user_id': u.user_id,
                    'name': u.name,
                    'email': u.email,
                    'state': (u.state.value if u.state is not None else None),
                    'role': (u.role.value if u.role is not None else None),
                    'active': (u.active.value if u.active is not None else None),
                    'ra': u.ra,
                    'course': (u.course.value if u.course is not None else None),
                    'year': u.year,
                    'organization': (u.organization.value if u.organization is not None else None),
                } for u in sorted(users, key=lambda x: x.name.casefold())
            ],
            'message': 'the users were retrieved'
        }

        assert viewmodel == expected
