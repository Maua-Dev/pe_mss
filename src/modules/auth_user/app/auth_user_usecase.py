from typing import Tuple
from src.shared.domain.entities.user import User
from src.shared.domain.repositories.user_repository_interface import IUserRepository
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import NoItemsFound


class AuthUserUsecase:
    def __init__(self, repo: IUserRepository):
        self.repo = repo

    def __call__(self, user: User) -> Tuple[User, int]:
        
        try:
            
            matched_user = self.repo.get_user_by_email(email=user.email)
        
            if matched_user:
                
                if matched_user.user_id != user.user_id:
                    # Reallocate user ID to match token ID
                    updated_user = self.repo.reallocate_id(user_id=user.user_id, email=user.email)
                    return (updated_user, 0)
                return (matched_user, 0)
            
        except NoItemsFound:
            created_user= self.repo.create_user(new_user=user)
            return (created_user, 1)
