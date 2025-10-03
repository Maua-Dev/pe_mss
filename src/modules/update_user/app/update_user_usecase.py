from src.shared.domain.entities.user import User
from src.shared.domain.enums.course_enum import COURSE
from src.shared.domain.enums.organization_enum import ORGANIZATION
from src.shared.domain.enums.role_enum import ROLE
from src.shared.domain.enums.state_enum import STATE
from src.shared.domain.repositories.user_repository_interface import IUserRepository
from src.shared.helpers.errors.domain_errors import EntityError


class UpdateUserUsecase:
    def __init__(self, repo: IUserRepository):
        self.repo = repo

    def __call__(self, name: str, email: str, ra: str, new_state: STATE, new_role: ROLE, new_course: COURSE=None, new_year: int=None, new_organization: ORGANIZATION=None, user_id: str=None) -> User:

        if type(name) != str or name.strip() == "":
            raise EntityError("new_name")
        
        if type(email) != str or email.strip() == "":
            raise EntityError("email")
        
        if type(ra) != str or ra.strip() == "":
            raise EntityError("ra")

        if type(new_state) != STATE:
            raise EntityError("state")
        
        if type(new_role) != ROLE:
            raise EntityError("role")
        
        if type(new_course) != COURSE and new_course is not None:
            raise EntityError("course")
        
        if type(new_year) != int and new_year is not None:
            raise EntityError("year")
        
        if type(new_organization) != ORGANIZATION and new_organization is not None:
            raise EntityError("entity")
        
        if not User.validate_id(user_id) and user_id is not None:
            raise EntityError("user_id")

        updated_user = self.repo.update_user(
            user_id=user_id,
            new_state=new_state,
            new_role=new_role,
            new_course=new_course,
            new_year=new_year,
            new_organization=new_organization
        )

        return updated_user
