from src.modules.update_user.app.update_user_viewmodel import UpdateUserViewmodel
from src.shared.domain.entities.user import User
from src.shared.domain.enums.course_enum import COURSE
from src.shared.domain.enums.active_enum import ACTIVE
from src.shared.domain.enums.organization_enum import ORGANIZATION
from src.shared.domain.enums.role_enum import ROLE
from src.shared.domain.enums.state_enum import STATE


class Test_UpadateUserViewmodel:
    def test_update_user_viewmodel(self):
        user = User(name="Test", active=ACTIVE.ACTIVE, user_id="550e8400-e29b-41d4-a716-446655440001", email="23.00768-0@maua.br", state=STATE.APPROVED, ra="23.00768-0", course=COURSE.CIC, year=4, role=ROLE.USER, organization=ORGANIZATION.DEV, )

        updated_user_viewmodel = UpdateUserViewmodel(user)

        expected = {
            
            'name': "Test",
            'email': "23.00768-0@maua.br",
            'ra': "23.00768-0",
            'state': STATE.APPROVED.value,
            'course': COURSE.CIC,
            'year': 4,
            'role': ROLE.USER,
            'organization': ORGANIZATION.DEV,
            'active': ACTIVE.ACTIVE.value,
            'user_id': "550e8400-e29b-41d4-a716-446655440001",

            'message': "the user was updated successfully"
        }

        assert expected == updated_user_viewmodel.to_dict()
