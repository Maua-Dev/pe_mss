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
        
    def _validate_enum(self, enum_class, value: Optional[str], field_name: str):
        if value is None:
            return None
        try:
            return enum_class(value)
        except ValueError:
            # TODO change this to a more specific raise
            raise NoItemsFound(f"{field_name}: '{value}' is not a valid {enum_class.__name__} value.")

    def __call__(
        self, 
        user_id: str, 
        name: Optional[str] = None,
        ra: Optional[str] = None,
        state: Optional[str] = None,
        role: Optional[str] = None,
        active: Optional[str] = None,
        course: Optional[str] = None,
        year: Optional[int] = None,
        organization: Optional[str] = None,
    ) -> list | int:
        
        user = self.userrepo.get_user(user_id)
        if user is None:
            raise NoItemsFound(user_id)
        
        is_active = True if user.active == ACTIVE.ACTIVE else False

        if not is_active:
            raise ForbiddenAction("Inactive users cannot perform this action.")
        
        requester_role = user.role
        
        state = self._validate_enum(STATE, state, "state")
        role = self._validate_enum(ROLE, role, "role")
        active = self._validate_enum(ACTIVE, active, "active")
        course = self._validate_enum(COURSE, course, "course")
        organization = self._validate_enum(ORGANIZATION, organization, "organization")

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
        
        return users, requester_role