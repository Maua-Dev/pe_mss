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

    def __call__(self, name: str, email: str, ra: str, state: STATE, role: ROLE, course: COURSE=None, year: int=None, organization: ORGANIZATION=None, user_id: str=None) -> User:

        if type(name) != str or name.strip() == "":
            raise EntityError("name")
        
        if type(email) != str or email.strip() == "":
            raise EntityError("email")
        
        if type(ra) != str or ra.strip() == "":
            raise EntityError("ra")

        if type(state) != STATE:
            raise EntityError("state")
        
        if type(role) != ROLE:
            raise EntityError("role")
        
        if type(course) != COURSE and course is not None:
            raise EntityError("course")
        
        if type(year) != int and year is not None:
            raise EntityError("year")
        
        if type(organization) != ORGANIZATION and organization is not None:
            raise EntityError("entity")
        
        if not User.validate_id(user_id) and user_id is not None:
            raise EntityError("user_id")

        existing_user = self.repo.get_user(user_id)
        if existing_user is None:
            raise EntityError("user not found")

        updated_user = self.repo.update_user(
            user_id=user_id,
            new_state=state,
            new_role=role,
            new_course=course,
            new_year=year,
            new_organization=organization
        )

        return updated_user
