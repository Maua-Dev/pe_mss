from src.shared.domain.repositories.user_repository_interface import IUserRepository
from src.shared.domain.repositories.warning_repository_interface import IWarningRepository
from src.shared.helpers.errors.usecase_errors import NoItemsFound


class GetAllWarningsUseCase:
    def __init__(self, repo: IWarningRepository, user_repo: IUserRepository):
        self.repo = repo
        self.user_repo = user_repo

    def __call__(self):
        all_warnings = self.repo.get_all_warnings()

        if not all_warnings:
            raise NoItemsFound("warning repository.")
        
        return all_warnings