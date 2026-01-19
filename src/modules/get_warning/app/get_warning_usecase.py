from typing import List
from src.shared.domain.enums.organization_enum import ORGANIZATION
from src.shared.domain.enums.role_enum import ROLE
from src.shared.domain.repositories.user_repository_interface import IUserRepository
from src.shared.domain.repositories.warning_repository_interface import IWarningRepository
from src.shared.domain.entities.warning import Warning
from src.shared.helpers.errors.usecase_errors import NoItemsFound

class GetWarningUsecase:
    def __init__(self, repo: IWarningRepository, user_repo: IUserRepository):
        self.repo= repo
        self.user_repo= user_repo

    def __call__(self, warning_id:Warning=None, role:ROLE=None, organization:ORGANIZATION=None):
        if warning_id:
            warning= self.repo.get_warning(warning_id=warning_id)

        else:
            
            if role and not organization:
                warning = self.repo.get_warnings_by_role(target_role=role)
                
            elif organization and not role:
                warning = self.repo.get_warnings_by_org(target_org=organization)
                
            else:
                warning = self.repo.get_warnings_by_org_and_role(
                    target_role=role,
                    target_org=organization
                )

        if warning is None:
            raise NoItemsFound("the parameters")
        
        if isinstance(warning, list):
            return warning

        return [warning]