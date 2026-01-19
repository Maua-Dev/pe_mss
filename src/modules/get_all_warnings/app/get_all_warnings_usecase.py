from src.shared.domain.enums.role_enum import ROLE
from src.shared.domain.repositories.user_repository_interface import IUserRepository
from src.shared.domain.repositories.warning_repository_interface import IWarningRepository
from src.shared.helpers.errors.usecase_errors import ForbiddenAction, NoItemsFound


class GetAllWarningsUseCase:
    def __init__(self, repo: IWarningRepository, user_repo: IUserRepository):
        self.repo = repo
        self.user_repo = user_repo

    def __call__(self, user_id):

        if self.user_repo.get_user(user_id=user_id).role != ROLE.ADM:
            raise ForbiddenAction("Only ADM users can get all warnings.")

        all_warnings = self.repo.get_all_warnings()

        if not all_warnings:
            raise NoItemsFound("warning repository.")
        
        return all_warnings