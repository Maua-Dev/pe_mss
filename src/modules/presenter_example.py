# from .auth_user_controller import AuthUserController
# from .auth_user_usecase import AuthUserUsecase
# from src.shared.helpers.external_interfaces.http_lambda_requests import LambdaHttpRequest, LambdaHttpResponse
# from src.shared.environments import Environments

# repo = Environments.get_user_repo()()
# usecase = AuthUserUsecase(repo)
# controller = AuthUserController(usecase)


# def auth_user_presenter(event, context):
#     httpRequest = LambdaHttpRequest(data=event)
#     httpRequest.data['user_from_authorizer'] = event.get('requestContext', {}).get('authorizer', {}).get('user', None)
#     # essa linha acima é responsavel por extrarir o user do campo authorizer do evento. esse usuario é o usuario obtido pelo
#     # pelo token microsoft passado para o nosso authorizer em src.shared.authorizer
#     response = controller(httpRequest)
#     httpResponse = LambdaHttpResponse(status_code=response.status_code, body=response.body, headers=response.headers)

#     return httpResponse.toDict()


# def lambda_handler(event, context):
#     response = auth_user_presenter(event, context)

#     return response