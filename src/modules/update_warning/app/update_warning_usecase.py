from src.shared.clients.event_bridge_client import EventBridgeClient
from src.shared.domain.enums.role_enum import ROLE
from src.shared.domain.repositories.user_repository_interface import IUserRepository
from src.shared.domain.repositories.warning_repository_interface import IWarningRepository
from src.shared.domain.entities.warning import Warning, WarningBody
from src.shared.environments import Environments
from src.shared.helpers.errors.usecase_errors import ForbiddenAction

class UpdateWarningUsecase:
    def __init__(self, repo: IWarningRepository, user_repo: IUserRepository):
        self.repo = repo
        self.user_repo = user_repo

    def __call__(
        self,
        warning_id: str,

        title: str | None,
        description: str | None,
        user_id: str | None,
        expire: int | None = None,
        target_role: str | None = None,
        target_org: str | None = None) -> Warning:
        
        if self.user_repo.get_user(user_id=user_id).role != ROLE.ADM:
            raise ForbiddenAction("Only ADM users can update warnings.")
        
        original_warning = self.repo.get_warning(warning_id)
    
        if target_org:
            body= WarningBody(
                title=title if title else original_warning.body.title,
                description=description if description else original_warning.body.description,
                expire=expire if expire else original_warning.body.expire
            )

            warning= Warning(
                warning_id=warning_id,
                target_role=target_role if target_role else original_warning.target_role,
                target_org=target_org if target_org else original_warning.target_org,
                body=body
            )
        else:
            body= WarningBody(
                title=title if title else original_warning.body.title,
                description=description if description else original_warning.body.description,
                expire=expire if expire else original_warning.body.expire
            )

            warning= Warning(
                warning_id=warning_id ,
                target_role=target_role if target_role else original_warning.target_role,
                target_org=original_warning.target_org,
                body=body
            )
        
        if not Environments.get_envs().stage.value == "TEST" and original_warning.body.expire != expire:
            eb_client= EventBridgeClient()
            expire_timestamp_ms = expire
            
            eb_client.create_trigger_for_deletion(
                warning_id=warning.warning_id,
                expire=expire_timestamp_ms
            )

        updated_warning = self.repo.update_warning(warning_id, warning)
        return updated_warning