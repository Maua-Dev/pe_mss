from typing import Tuple
from src.shared.domain.entities.user import User
from src.shared.domain.repositories.user_repository_interface import IUserRepository
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import NoItemsFound


class AuthUserUsecase:
    def __init__(self, repo: IUserRepository):
        self.repo = repo

    def __call__(self, user: User) -> Tuple[User, int]:
        if type(user) != User:
            raise EntityError("user")
        try:
            get_user= self.repo.get_user(user_id=user.user_id)
            if type(get_user) == User:
                return (get_user, 0)
            
        except NoItemsFound:
            created_user= self.repo.create_user(new_user=user)
            return (created_user, 1)
