import json
from .create_user_controller import CreateUserController
from .create_user_usecase import CreateUserUsecase
from src.shared.environments import Environments
from src.shared.helpers.external_interfaces.http_lambda_requests import LambdaHttpRequest, LambdaHttpResponse

repo = Environments.get_user_repo()()
usecase = CreateUserUsecase(repo)
controller = CreateUserController(usecase)


def lambda_handler(event, context):
    httpRequest = LambdaHttpRequest(data=event)

    user_info_string = event.get('requestContext', {}).get('authorizer', {})
    
    if not user_info_string:
        httpRequest.data['user_from_authorizer'] = None
    elif isinstance(user_info_string, str):
        httpRequest.data['user_from_authorizer'] = json.loads(user_info_string).get('user')
    elif isinstance(user_info_string, dict):
        httpRequest.data['user_from_authorizer'] = user_info_string.get('user')
    else:
        httpRequest.data['user_from_authorizer'] = None
    
    response = controller(httpRequest)
    httpResponse = LambdaHttpResponse(status_code=response.status_code, body=response.body, headers=response.headers)

    return httpResponse.toDict()
