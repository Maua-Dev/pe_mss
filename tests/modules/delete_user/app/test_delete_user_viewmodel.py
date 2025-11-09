from src.modules.delete_user.app.delete_user_viewmodel import DeleteUserViewmodel
from src.shared.domain.entities.user import User
from src.shared.domain.enums.active_enum import ACTIVE
from src.shared.domain.enums.role_enum import ROLE
from src.shared.domain.enums.state_enum import STATE


class Test_DeleteUserViewmodel:
    def test_delete_user_viewmodel(self):
        user = User(user_id="632bd20f-ba30-41b1-904a-7df68f0daa70", name="Test", email="test@maua.br", state=STATE.PENDING, role=ROLE.USER, active=ACTIVE.ACTIVE, ra="00.00000-0")

        delete_user_viewmodel = DeleteUserViewmodel(user)

        expected = {
            "user": {
                'user_id': "632bd20f-ba30-41b1-904a-7df68f0daa70",
                'name': "Test",
                'email': "test@maua.br",
                'ra': "00.00000-0",
                'state': STATE.PENDING.value,
                'role': ROLE.USER.value,
                'active': ACTIVE.ACTIVE.value,
                'course': None,
                'organization': None,
            },
            'message': "the user was deleted successfully"
        }

        assert expected == delete_user_viewmodel.to_dict()