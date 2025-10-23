from src.shared.domain.entities.user import User
from src.shared.domain.enums.active_enum import ACTIVE
from src.shared.domain.enums.course_enum import COURSE
from src.shared.domain.enums.organization_enum import ORGANIZATION
from src.shared.domain.enums.role_enum import ROLE
from src.shared.domain.enums.state_enum import STATE


class GetUserViewModel:
    user_id: str    
    name: str
    email: str
    ra: str
    role: ROLE
    state: STATE
    course: COURSE
    year: int
    active: ACTIVE
    organization: ORGANIZATION

    def __init__(self, user: User):
        self.user_id = user.user_id
        self.name = user.name
        self.email = user.email
        self.ra = user.ra
        self.role = user.role
        self.state = user.state
        self.course = user.course
        self.year = user.year
        self.active = user.active
        self.organization = user.organization

    def to_dict(self):
        return {
            'user': {
                'user_id': self.user_id,
                'name': self.name,
                'email': self.email,
                'ra': self.ra,
                'role': self.role.value,
                'state': self.state.value,
                'course': self.course.value,
                'year': self.year,
                'active': self.active.value,
                'organization': self.organization.value,
            },
            "message": "the user was retrieved"
        }