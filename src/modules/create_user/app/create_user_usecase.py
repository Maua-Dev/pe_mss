from src.shared.domain.repositories.user_repository_interface import IUserRepository
from src.shared.domain.enums.role_enum import ROLE


class CreateUserUsecase:
    def __init__(self, repo: IUserRepository):
        self.repo = repo

    def __call__(self, user_data, case) -> IUserRepository.create_user:
        match case:
            case ROLE.ADM:
                new_user= self.repo.create_user(
                    new_user= user_data
                )
                return new_user

        # created_user= self.repo.create_user(new_user=new_user)
        # return created_user