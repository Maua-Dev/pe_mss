from typing import List, Optional, Any
from src.shared.domain.entities.user import User
from src.shared.domain.enums.active_enum import ACTIVE
from src.shared.domain.enums.course_enum import COURSE
from src.shared.domain.enums.organization_enum import ORGANIZATION
from src.shared.domain.enums.role_enum import ROLE
from src.shared.domain.enums.state_enum import STATE


class UserViewModel:
    user_id: Optional[str]
    name: str
    email: str
    ra: str
    role: ROLE
    active: Optional[ACTIVE] = None
    state: Optional[STATE] = None
    course: Optional[COURSE] = None
    year: Optional[int] = None
    organization: Optional[ORGANIZATION] = None

    def __init__(self, user: User, show_user_id: bool = True):
        self.user_id = user.user_id if show_user_id else None
        self.name = user.name
        self.email = user.email
        self.ra = user.ra
        self.role = user.role.value if user.role is not None else None
        self.active = user.active.value if user.active is not None else None
        self.state = user.state.value if user.state is not None else None
        self.course = user.course.value if user.course is not None else None
        self.year = user.year if user.year is not None else None
        self.organization = user.organization.value if user.organization is not None else None

    def to_dict(self):
        data = {
            "user_id": self.user_id,
            "name": self.name,
            "email": self.email,
            "state": self.state,
            "role": self.role,
            "active": self.active,
            "ra": self.ra,
            "course": self.course,
            "year": self.year,
            "organization": self.organization
        }
        
        if data["user_id"] is None:
            del data["user_id"]
            
        return data

class GetUserViewModel:
    user: UserViewModel

    def __init__(self, user: User, show_user_id: bool = True):
        self.user = UserViewModel(user, show_user_id=show_user_id)

    def to_dict(self):
        return {
            "user": self.user.to_dict()
        }


class GetAllUsersViewModel:
    users: List[UserViewModel]

    def __init__(self, users: List[User], requester_role: ROLE, requester_id: Optional[str] = None):
        self.users = []

        requester_role_name = requester_role

        for user in users:
            if requester_role_name is None:
                show_user_id = True
            elif requester_role_name in [ROLE.ADM, ROLE.PRESIDENT]:
                show_user_id = True
            else:
                show_user_id = (user.user_id == requester_id)
            self.users.append(UserViewModel(user, show_user_id=show_user_id))

    def to_dict(self):
        return {
            "users": [user.to_dict() for user in self.users],
            "message": "the users were retrieved"
        }
