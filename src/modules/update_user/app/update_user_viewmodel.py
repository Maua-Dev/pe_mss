from src.shared.domain.entities.user import User
from src.shared.domain.enums.active_enum import ACTIVE
from src.shared.domain.enums.course_enum import COURSE
from src.shared.domain.enums.organization_enum import ORGANIZATION
from src.shared.domain.enums.role_enum import ROLE
from src.shared.domain.enums.state_enum import STATE

class UpdateUserViewmodel:

    name: str
    email: str
    ra: str
    state: STATE
    course: COURSE
    year: int
    role: ROLE
    organization: ORGANIZATION
    active: ACTIVE
    user_id: str

    def __init__(self, user: User):
        
        self.name = user.name
        self.email = user.email
        self.ra  = user.ra
        self.state = user.state
        self.course = user.course
        self.year = user.year
        self.role = user.role
        self.organization = user.organization
        self.active = user.active
        self.user_id = user.user_id

    def to_dict(self):
        return {
            'name': self.name,
            'email': self.email,
            'ra': self.ra,
            'state': self.state.value if self.state else None,
            'course': self.course.value if self.course else None,
            'year': self.year,
            'role': self.role.value if self.role else None,
            'organization': self.organization.value if self.organization else None,
            'active': self.active.value if self.active else None,
            'user_id': self.user_id,
            'message': "the user was updated successfully"
        }
    
