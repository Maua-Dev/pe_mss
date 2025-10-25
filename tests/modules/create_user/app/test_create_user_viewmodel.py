from src.modules.create_user.app.create_user_viewmodel import CreateUserViewmodel
from src.shared.domain.entities.user import User
from src.shared.domain.enums.active_enum import ACTIVE
from src.shared.domain.enums.organization_enum import ORGANIZATION
from src.shared.domain.enums.role_enum import ROLE
from src.shared.domain.enums.state_enum import STATE


class Test_CreateUserViewmodel:
    def test_create_user_viewmodel(self):
        user = User(
            user_id='550e8400-e29b-41d4-a716-446655440003',
            name='Maria',
            email='21.00100-2@maua.br',
            organization=ORGANIZATION.DEV,
            role=ROLE.USER,
            state=STATE.PENDING,
            ra='21.00100-2',
            active=ACTIVE.ACTIVE,
        )

        user_viewmodel = CreateUserViewmodel(user=user)
        
        assert user_viewmodel.user_or_users == user
        assert not user_viewmodel.is_list
        
    def test_create_user_viewmodel_case_planilha(self):
        user1 = User(
            user_id='550e8400-e29b-41d4-a716-446655440004',
            name='Ana',
            email='21.00100-2@maua.br',
            organization=ORGANIZATION.DEV,
            role=ROLE.USER,
            state=STATE.PENDING,
            ra='21.00100-2',
            active=ACTIVE.ACTIVE,
        )   

        user2 = User(
            user_id='550e8400-e29b-41d4-a716-446655440005',
            name='Carlos',
            email='21.00100-3@maua.br',
            organization=ORGANIZATION.DEV,
            role=ROLE.USER,
            state=STATE.PENDING,
            ra='21.00100-3',
            active=ACTIVE.ACTIVE,
        )

        user_viewmodel = CreateUserViewmodel(user=user1)

        assert user_viewmodel.user_or_users == user1
        assert not user_viewmodel.is_list

        user_viewmodel = CreateUserViewmodel(user=[user1, user2])

        assert user_viewmodel.user_or_users == [user1, user2]
        assert user_viewmodel.is_list
        
    def test_create_user_viewmodel_to_dict(self):
        user = User(
            user_id='550e8400-e29b-41d4-a716-446655440006',
            name='Maria',
            email='21.00100-2@maua.br',
            organization=ORGANIZATION.DEV,
            role=ROLE.USER,
            state=STATE.PENDING,
            ra='21.00100-2',
            active=ACTIVE.ACTIVE,
        )

        user_viewmodel = CreateUserViewmodel(user=user)

        assert user_viewmodel.to_dict() == {
            "user": {
                'user_id': '550e8400-e29b-41d4-a716-446655440006',
                'name': 'Maria',
                'email': '21.00100-2@maua.br',
                'organization': ORGANIZATION.DEV.value,
                'role': ROLE.USER.value,
                'state': STATE.PENDING.value,
                'ra': '21.00100-2',
                'active': ACTIVE.ACTIVE.value,
                'course': None
            },
            "message": "the user was created successfully"
        }
