from typing import List
from src.shared.domain.entities.user import User

from src.shared.domain.enums.state_enum import STATE
from src.shared.domain.repositories.user_repository_interface import IUserRepository
from src.shared.helpers.errors.usecase_errors import NoItemsFound
from src.shared.domain.enums.course_enum import COURSE
from src.shared.domain.enums.organization_enum import ORGANIZATION
from src.shared.domain.enums.role_enum import ROLE


class UserRepositoryMock(IUserRepository):
    users: List[User]
    
    def __init__(self):
        self.users = [
            User(name="Guilherme",email="25.00178-5@maua.br", ra="25.00178-5", state=STATE.PENDING, role=ROLE.USER, user_id="550e8400-e29b-41d4-a716-446655440000"),
            User(name="João",email="21.00678-2@maua.br", ra="24.00678-2", state=STATE.APPROVED, role=ROLE.ADM, course=COURSE.CIC, year=4, organization=ORGANIZATION.DEV, user_id="550e8400-e29b-41d4-a716-446655440001"),
            User(name="Heitor", email="21.00453-7@maua.br", ra="21.00453-7", state=STATE.APPROVED, role=ROLE.USER, course=COURSE.ECM, year=4, organization=ORGANIZATION.DEV, user_id="550e8400-e29b-41d4-a716-446655440002"),
            User(name="Bruno", email="21.00458-7@maua.br", ra="21.00458-7", state=STATE.REJECTED, role=ROLE.PRESIDENT, course=COURSE.EET, year=1, organization=ORGANIZATION.GUARDIAN, user_id="550e8400-e29b-41d4-a716-446655440003")
        ]
    
    def delete_user(self, user_id: str):
        for pos, user in enumerate(self.users):
            if user.user_id == user_id:
                self.users.pop(pos)
                return user
        raise NoItemsFound(user_id)
            
    def update_user(self, user_id: str, new_state: STATE =None, new_role: ROLE =None, new_course: COURSE=None, new_year: int=None,  new_organization: ORGANIZATION=None):
        for user in self.users:
            if user.user_id == user_id:
                if new_state != None:
                    user.state= new_state
                if new_role != None:
                    user.role= new_role
                if new_course != None:
                    user.course= new_course
                if new_year != None:
                    user.year= new_year
                if new_organization != None:
                    user.organization= new_organization
                return user
        raise NoItemsFound(user_id)