from src.shared.domain.entities.user import User
from src.shared.domain.enums.active_enum import ACTIVE
from src.shared.domain.repositories.user_repository_interface import IUserRepository
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import ForbiddenAction, NoItemsFound


class GetUserUsecase:
    def __init__(self, user_repo: IUserRepository):
        self.user_repo = user_repo

    def __call__(self, user_id: str) -> User:
        
        if not User.validate_id(user_id):
            raise EntityError("user_id")
        
        user = self.user_repo.get_user(user_id = user_id)

        if user == None:
            raise NoItemsFound(user_id)
        
        is_active = True if user.active == ACTIVE.ACTIVE else False

        if not is_active:
            raise ForbiddenAction("Inactive users cannot perform this action.")
        
        return user