from src.modules.auth_user.app.auth_user_controller import AuthUserController
from src.modules.auth_user.app.auth_user_usecase import AuthUserUsecase
from src.shared.environments import Environments
from src.shared.helpers.external_interfaces.http_lambda_requests import LambdaHttpRequest, LambdaHttpResponse

repo = Environments.get_user_repo()()
usecase = AuthUserUsecase(repo)
controller = AuthUserController(usecase)


def lambda_handler(event, context):
    httpRequest = LambdaHttpRequest(data=event)
    httpRequest.data['user_from_authorizer']= event.get('requestContext', {}).get('authorizer', {}).get('user', None)
    response = controller(httpRequest)
    httpResponse = LambdaHttpResponse(status_code=response.status_code, body=response.body, headers=response.headers)

    return httpResponse.toDict()
