from src.shared.domain.entities.user import User
from src.shared.domain.enums.state_enum import STATE
from src.shared.domain.enums.role_enum import ROLE
from src.shared.domain.enums.course_enum import COURSE
from src.shared.domain.enums.organization_enum import ORGANIZATION
from src.shared.domain.enums.active_enum import ACTIVE

class CreateUserViewmodel:
    user_id: str
    name: str
    email: str
    state: STATE
    role: ROLE
    ra: str
    case_number: int
    active: ACTIVE
    course: COURSE
    organization: ORGANIZATION

    def __init__(self, user: User):
        self.user_id= user.user_id
        self.name= user.name
        self.email= user.email
        self.ra= user.ra
        self.state= user.state
        self.role= user.role
        self.active= user.active
        self.organization= user.organization
        self.active = user.active
        self.course = user.course
    
    def to_dict(self):
        model={
            'user_id': self.user_id,
            'name': self.name,
            'email': self.email,
            'ra': self.ra,
            'state': self.state.value if self.state is not None else None,
            'role': self.role.value if self.state is not None else None,
            'organization': self.organization.value if self.organization is not None else None,
            'active': self.active.value if self.active is not None else None,
            'course': self.course.value if self.course is not None else None
        }

        model.update({'message': "the user was created successfully"})
        return model