import json
import logging
from .update_user_controller import UpdateUserController
from .update_user_usecase import UpdateUserUsecase
from src.shared.environments import Environments
from src.shared.helpers.external_interfaces.http_lambda_requests import LambdaHttpRequest, LambdaHttpResponse

logger = logging.getLogger()
logger.setLevel(logging.INFO)

repo = Environments.get_user_repo()
usecase = UpdateUserUsecase(repo)
controller = UpdateUserController(usecase)


def lambda_handler(event, context):
    httpRequest = LambdaHttpRequest(data=event)

    httpRequest = LambdaHttpRequest(data=event)
    
    logger.info("Iniciando auth_user_presenter lambda_handler.")

    user_graph_info_raw = (
        event.get("requestContext", {})
             .get("authorizer", {})
             .get("user")
    )

    logger.info("Informações do usuário extraídas com sucesso.")
    logger.info(f"Raw user info: {user_graph_info_raw}")

    user_info = None
    if isinstance(user_graph_info_raw, str):
        try:
            user_info = json.loads(user_graph_info_raw)
        except json.JSONDecodeError:
            user_info = None
    elif isinstance(user_graph_info_raw, dict):
        user_info = user_graph_info_raw

    httpRequest.data["user_from_authorizer"] = user_info
    
    logger.info("User info decoded successfully.")
    logger.debug(f"Decoded user info: {user_info}")

    print("Decoded user:", user_info)

    response = controller(httpRequest)
    httpResponse = LambdaHttpResponse(
        status_code=response.status_code,
        body=response.body,
        headers=response.headers
    )

    return httpResponse.toDict()
