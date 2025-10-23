import json
from .get_all_users_controller import GetAllUsersController
from .get_all_users_usecase import GetAllUsersUsecase
from src.shared.environments import Environments
from src.shared.helpers.external_interfaces.http_lambda_requests import LambdaHttpRequest, LambdaHttpResponse


userrepo = Environments.get_user_repo()
usecase = GetAllUsersUsecase(userrepo=userrepo)
controller = GetAllUsersController(usecase=usecase)

def lambda_handler(event, context):
    httpRequest = LambdaHttpRequest(data=event)

    user_info_string = event.get('requestContext', {}).get('authorizer', {}).get('user', None)
    
    if not user_info_string:
        httpRequest.data['user_from_authorizer'] = None
    elif isinstance(user_info_string, str):
        httpRequest.data['user_from_authorizer'] = json.loads(user_info_string)
    elif isinstance(user_info_string, dict):
        httpRequest.data['user_from_authorizer'] = user_info_string
    else:
        httpRequest.data['user_from_authorizer'] = None
    
    response = controller(httpRequest)
    httpResponse = LambdaHttpResponse(status_code=response.status_code, body=response.body, headers=response.headers)

    return httpResponse.toDict()