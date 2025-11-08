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
                 
                requester_id: str,
                target_id: str,
                 
                new_state: Optional[str] = None, 
                new_role: Optional[str] = None, 
                new_course: Optional[str] = None,
                new_year: Optional[int] = None, 
                new_organization: Optional[str] = None, 
                new_active: Optional[str] = None) -> User:

        if User.validate_id(target_id) is False:
            raise EntityError("user_id")

        if User.validate_id(requester_id) is False:
            raise EntityError("requester_id")
        
        # raise for not found user
        self.repo.get_user(user_id=target_id)

        self.repo.has_permission_target_id(
            requester_id=requester_id,
            target_id=target_id
        )

        if new_state is not None:

            try:  

                new_state = STATE(new_state)

            except ValueError:

                raise EntityError("state")

        if new_role is not None:

            try:  

                new_role = ROLE(new_role)

            except ValueError:

                raise EntityError("role")
            
        if new_course is not None:

            try:  

                new_course = COURSE(new_course)

            except ValueError:

                raise EntityError("course")
            
        if new_year is not None:

            if type(new_year) != int:
                raise EntityError("year")
        
        if new_organization is not None:

            try:  

                new_organization = ORGANIZATION(new_organization)

            except ValueError:

                raise EntityError("organization")
            
        if new_active is not None:

            try:  

                new_active = ACTIVE(new_active)

            except ValueError:

                raise EntityError("active")

        updated_user = self.repo.update_user(
            user_id=target_id,
            new_state=new_state,
            new_role=new_role,
            new_course=new_course,
            new_year=new_year,
            new_organization=new_organization,
            new_active=new_active
        )

        return updated_user
