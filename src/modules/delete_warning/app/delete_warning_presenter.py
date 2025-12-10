import json
from src.modules.delete_warning.app.delete_warning_controller import DeleteWarningController
from src.modules.delete_warning.app.delete_warning_usecase import DeleteWarningUsecase
from src.shared.environments import Environments
from src.shared.helpers.external_interfaces.http_lambda_requests import LambdaHttpRequest, LambdaHttpResponse

repo= Environments.get_warning_repo()
user_repo= Environments.get_user_repo()

usecase= DeleteWarningUsecase(repo, user_repo)
controller= DeleteWarningController(usecase)

def lambda_handler(event, context):
    httpRequest= LambdaHttpRequest(data=event)

    user_graph_info_raw = (
        event.get("requestContext", {})
             .get("authorizer", {})
             .get("user")
    )

    user_info = None
    if isinstance(user_graph_info_raw, str):
        try:
            user_info = json.loads(user_graph_info_raw)
        except json.JSONDecodeError:
            user_info = None
    elif isinstance(user_graph_info_raw, dict):
        user_info = user_graph_info_raw

    httpRequest.data["user_from_authorizer"] = user_info

    response= controller(httpRequest)
    httpResponse= LambdaHttpResponse(
        status_code= response.status_code,
        body= response.body,
        headers= response.headers
    )

    return httpResponse.toDict()