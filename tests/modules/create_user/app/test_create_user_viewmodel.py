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

        assert user_viewmodel.user_id == '550e8400-e29b-41d4-a716-446655440003'
        assert user_viewmodel.name == 'Maria'
        assert user_viewmodel.email == '21.00100-2@maua.br'
        assert user_viewmodel.organization == ORGANIZATION.DEV
        assert user_viewmodel.role == ROLE.USER
        assert user_viewmodel.state == STATE.PENDING
        assert user_viewmodel.ra == '21.00100-2'
        assert user_viewmodel.active == ACTIVE.ACTIVE