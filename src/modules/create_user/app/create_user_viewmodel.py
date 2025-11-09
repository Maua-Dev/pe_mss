from src.shared.domain.entities.user import User
from src.shared.domain.enums.state_enum import STATE
from src.shared.domain.enums.role_enum import ROLE
from src.shared.domain.enums.course_enum import COURSE
from src.shared.domain.enums.organization_enum import ORGANIZATION
from src.shared.domain.enums.active_enum import ACTIVE


class CreateUserViewmodel:
    def __init__(self, user: User | list[User]):
        self.is_list = isinstance(user, list)
        self.user_or_users = user

    def _user_to_dict(self, user: User):
        return {
            "user": {
                "user_id": user.user_id,
                "name": user.name,
                "email": user.email,
                "ra": user.ra,
                "state": user.state.value if user.state else None,
                "role": user.role.value if user.role else None,
                "organization": user.organization.value if user.organization else None,
                "active": user.active.value if user.active else None,
                "course": user.course.value if user.course else None
            }
        }

    def to_dict(self):
        if self.is_list:
            return {
                "users": [self._user_to_dict(u) for u in self.user_or_users],
                "message": "the users were created successfully"
            }

        return {
            **self._user_to_dict(self.user_or_users),
            "message": "the user was created successfully"
        }
