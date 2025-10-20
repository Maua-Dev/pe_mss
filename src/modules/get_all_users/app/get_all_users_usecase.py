from typing import Optional
from src.shared.domain.entities.user import User
from src.shared.domain.enums.active_enum import ACTIVE
from src.shared.domain.enums.course_enum import COURSE
from src.shared.domain.enums.organization_enum import ORGANIZATION
from src.shared.domain.enums.role_enum import ROLE
from src.shared.domain.enums.state_enum import STATE
from src.shared.domain.repositories.user_repository_interface import IUserRepository
from src.shared.helpers.errors.usecase_errors import NoItemsFound, ForbiddenAction


class GetAllUsersUsecase:
    def __init__(self, userrepo: IUserRepository):
        self.userrepo = userrepo

    def __call__(self, 
                 user_id: str, 
                 name: Optional[str] = None,
                  ra: Optional[str] = None,
                  state: Optional[STATE] = None,
                  role: Optional[ROLE] = None,
                  active: Optional[ACTIVE] = None,
                  course: Optional[COURSE] = None,
                  year: Optional[int] = None,
                  organization: Optional[ORGANIZATION] = None,
                  ) -> list:
        
        user = self.userrepo.get_user(user_id)
        if user is None:
            raise NoItemsFound(user_id)
        
        is_active = User.validate_active(user.active)

        if not is_active:
            raise ForbiddenAction("Inactive users cannot perform this action.")

        users = self.userrepo.get_users(
            name = name if name else None,
            ra = ra if ra else None,
            state = state if state else None,
            role = role if role else None,
            active = active if active else None,
            course = course if course else None,
            year = year if year else None,
            organization = organization if organization else None
        )

        if users is None or users == []:
            raise NoItemsFound("user filters passed.")
        
        users = sorted(users, key=lambda x: x.name.casefold())
        
        return users