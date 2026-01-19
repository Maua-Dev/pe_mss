import uuid
from src.shared.clients.event_bridge_client import EventBridgeClient
from src.shared.domain.entities.warning import WarningBody, Warning
from src.shared.domain.enums.role_enum import ROLE
from src.shared.domain.repositories.user_repository_interface import IUserRepository
from src.shared.domain.repositories.warning_repository_interface import IWarningRepository
from src.shared.environments import Environments
from src.shared.helpers.errors.usecase_errors import ForbiddenAction


class CreateWarningUsecase:
    def __init__ (self, repo: IWarningRepository, user_repo: IUserRepository):
        self.repo = repo
        self.user_repo = user_repo

    def __call__(
        self,
        title,
        description,
        expire,
        target_role,
        user_id,
        target_org=None
    ):
        
        if self.user_repo.get_user(user_id=user_id).role != ROLE.ADM:
            raise ForbiddenAction("Only ADM users can create warnings.")
        
        if target_org:
            body= WarningBody(
                title=title,
                description=description,
                expire=expire
            )

            warning= Warning(
                warning_id=str(uuid.uuid4()),
                target_role=target_role, # this is already ROLE enum
                target_org=target_org, # this is already ORGANIZATION enum
                body=body
                # created_at is being set automatically
            )
        else:
            body= WarningBody(
                title=title,
                description=description,
                expire=expire
            )

            warning= Warning(
                warning_id=str(uuid.uuid4()),
                target_role=target_role, # this is already ROLE enum
                # created_at is being set automatically
                body=body
            )
        
        if not Environments.get_envs().stage.value == "TEST":
            eb_client= EventBridgeClient()
            expire_timestamp_ms = expire
            
            rule = eb_client.create_trigger_for_deletion(
                warning_id=warning.warning_id,
                expire=expire_timestamp_ms
            )

        new_warning = self.repo.create_warning(new_warning=warning)
        return new_warning    