from src.shared.clients.event_bridge_client import EventBridgeClient
from src.shared.domain.repositories.user_repository_interface import IUserRepository
from src.shared.domain.repositories.warning_repository_interface import IWarningRepository
from src.shared.environments import Environments
from src.shared.helpers.errors.usecase_errors import NoItemsFound


class DeleteWarningUsecase:
    def __init__(self, repo:IWarningRepository, user_repo:IUserRepository):
        self.repo= repo
        self.user_repo= user_repo

    def __call__(
        self,
        warning_id
    ):
        
        if not Environments.get_envs().stage.value == "TEST":
            try:
                eb_client= EventBridgeClient()

                rule_name= f"one-time-trigger-for-alert-{warning_id}"

                rule= eb_client.delete_trigger(rule_name=rule_name)

            except Exception as e:

                raise Exception(f"Falha ao deletar o gatilho no EventBridge para a regra {rule_name}. Erro original: {e}")
            
        deleted_warning= self.repo.delete_warning(warning_id=warning_id)

        if deleted_warning == None:
            raise NoItemsFound("No warning found to be deleted")

        return deleted_warning