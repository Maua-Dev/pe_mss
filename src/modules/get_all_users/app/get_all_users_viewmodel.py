from src.shared.domain.entities.user import User
from src.shared.domain.enums.active_enum import ACTIVE
from src.shared.domain.enums.course_enum import COURSE
from src.shared.domain.enums.organization_enum import ORGANIZATION
from src.shared.domain.enums.role_enum import ROLE
from src.shared.domain.enums.state_enum import STATE


class UserViewModel:
        user_id: str
        name: str
        email: str
        state: STATE
        role: ROLE
        active: ACTIVE
        ra: str = None  
        course: COURSE=None 
        year: int=None 
        organization: ORGANIZATION=None

        def __init__(self, user: User):
            self.user_id = user.user_id
            self.name = user.name
            self.email = user.email
            self.state = user.state.value if user.state is not None else None
            self.role = user.role.value if user.role is not None else None
            self.active = user.active.value if user.active is not None else None
            self.ra = user.ra
            self.course = user.course.value if user.course is not None else None
            self.year = user.year
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

            return data
        
class GetUserViewModel:
    user: UserViewModel

    def __init__(self, user: User):
         self.user = UserViewModel(user)

    def to_dict(self):
         return {
              'user': self.user.to_dict()
         }
    
class GetAllUsersViewModel:
    users: list[UserViewModel]

    def __init__(self, users: list[User]):
        self.users = [UserViewModel(user) for user in users]

    def to_dict(self):
        return {
            'users': [user.to_dict() for user in self.users],
            'message': 'the users were retrieved'
        }