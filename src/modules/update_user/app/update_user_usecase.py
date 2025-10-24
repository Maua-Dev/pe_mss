from typing import Optional
from src.shared.domain.entities.user import User
from src.shared.domain.enums.course_enum import COURSE
from src.shared.domain.enums.organization_enum import ORGANIZATION
from src.shared.domain.enums.role_enum import ROLE
from src.shared.domain.enums.active_enum import ACTIVE
from src.shared.domain.enums.state_enum import STATE
from src.shared.domain.repositories.user_repository_interface import IUserRepository
from src.shared.helpers.errors.domain_errors import EntityError


class UpdateUserUsecase:
    def __init__(self, repo: IUserRepository):
        self.repo = repo

    def __call__(self, 
                user_id: str, 
                new_state: Optional[STATE] = None, 
                new_role: Optional[ROLE] = None, 
                new_course: Optional[COURSE] = None,
                new_year: Optional[int] = None, 
                new_organization: Optional[ORGANIZATION] = None, 
                new_active: Optional[ACTIVE] = None) -> User:

        if type(user_id) != str or not User.validate_id(user_id):
            raise EntityError("user_id")

        if new_state is not None and type(new_state) != STATE:
            raise EntityError("state")

        if new_role is not None and type(new_role) != ROLE:
            raise EntityError("role")

        if new_course is not None and type(new_course) != COURSE:
            raise EntityError("course")

        if new_year is not None and type(new_year) != int:
            raise EntityError("year")

        if new_organization is not None and type(new_organization) != ORGANIZATION:
            raise EntityError("organization")
        
        if new_active is not None and type(new_active) != ACTIVE:
            raise EntityError("active")

        updated_user = self.repo.update_user(
            user_id=user_id,
            new_state=new_state,
            new_role=new_role,
            new_course=new_course,
            new_year=new_year,
            new_organization=new_organization,
            new_active=new_active
        )

        return updated_user
