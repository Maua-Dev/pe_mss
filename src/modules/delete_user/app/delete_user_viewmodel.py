from src.shared.domain.entities.user import User
from src.shared.domain.enums.state_enum import STATE


class DeleteUserViewmodel:
    user: User

    def __init__(self, user: User):
        self.user = user

    def to_dict(self):
        return {
            "user": {
                'user_id': self.user.user_id,
                'name': self.user.name,
                'email': self.user.email,
                'ra': self.user.ra,
                'state': self.user.state.value if self.user.state else None,
                'role': self.user.role.value if self.user.role else None,
                'organization': self.user.organization.value if self.user.organization else None,
                'active': self.user.active.value if self.user.active else None,
                'course': self.user.course.value if self.user.course else None,
            },
            'message': "the user was deleted successfully"
        }

