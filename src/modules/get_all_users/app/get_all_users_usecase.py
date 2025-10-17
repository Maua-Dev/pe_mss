from typing import Optional
from src.shared.domain.entities.user import User
from src.shared.domain.enums.organization_enum import ORGANIZATION
from src.shared.domain.enums.state_enum import STATE
from src.shared.domain.repositories.user_repository_interface import IUserRepository
from src.shared.helpers.errors.usecase_errors import NoItemsFound, UserNotAllowed


class GetAllUsersUseCase:
    def __init__(self, userrepo: IUserRepository):
        self.userrepo = userrepo

    def __call__(self, user_id: str, organization: Optional[ORGANIZATION] = None, state: Optional[STATE] = None) -> list:
        user = self.userrepo.get_user(user_id)
        if user is None:
            raise NoItemsFound(user_id)
        
        is_active = User.validate_active(user.active)

        if not is_active:
            raise UserNotAllowed()

        users = self.userrepo.get_all_users()

        if organization is not None:
            users = [u for u in users if u.organization == organization]

        if state is not None:
            users = [u for u in users if u.state == state]

        return users