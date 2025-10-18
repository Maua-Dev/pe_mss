import json
from .create_user_controller import CreateUserController
from .create_user_usecase import CreateUserUsecase
from src.shared.environments import Environments
from src.shared.helpers.external_interfaces.http_lambda_requests import LambdaHttpRequest, LambdaHttpResponse

repo = Environments.get_user_repo()
usecase = CreateUserUsecase(repo)
controller = CreateUserController(usecase)


def lambda_handler(event, context):
    httpRequest = LambdaHttpRequest(data=event)

    # pega a string JSON
    user_graph_info_raw = (
        event.get("requestContext", {})
             .get("authorizer", {})
             .get("user_graph_info")
    )

    user_info = None
    if isinstance(user_graph_info_raw, str):
        try:
            # transforma a string JSON em dict
            user_info = json.loads(user_graph_info_raw)
        except json.JSONDecodeError:
            user_info = None
    elif isinstance(user_graph_info_raw, dict):
        user_info = user_graph_info_raw

    # salva no request
    httpRequest.data["user_from_authorizer"] = user_info

    # log opcional
    print("Decoded user:", user_info)

    response = controller(httpRequest)
    httpResponse = LambdaHttpResponse(
        status_code=response.status_code,
        body=response.body,
        headers=response.headers
    )

    return httpResponse.toDict()
