from src.shared.domain.entities.user import User
from src.shared.domain.enums.state_enum import STATE
from src.shared.domain.enums.role_enum import ROLE
from src.shared.domain.enums.course_enum import COURSE
from src.shared.domain.enums.organization_enum import ORGANIZATION
from src.shared.domain.enums.active_enum import ACTIVE

class AuthUserViewmodel:
    id: str
    name: str
    email: str
    state: STATE
    role: ROLE
    ra: str
    case_number: int
    active: ACTIVE
    course: COURSE
    organization: ORGANIZATION

    def __init__(self, user: User, case_number: int):
        self.id= user.user_id
        self.name= user.name
        self.email= user.email
        self.ra= user.ra
        self.state= user.state
        self.role= user.role
        self.active= user.active
        self.organization= user.organization
        self.case_number= case_number
        self.active = user.active
        self.course = user.course
    
    def to_dict(self):
        model={
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'ra': self.ra,
            'state': self.state.value,
            'role': self.role.value,
            'organization': self.organization.value,
            'active': self.active.value,
            'course': self.course.value

        }

        if self.case_number == 0:
            model.update({'message': "the user was retrieved successfully"})
            return model
        elif self.case_number == 1:
            model.update({'message': "the user was created successfully"})
            return model