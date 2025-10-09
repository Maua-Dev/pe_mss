# from .upload_users_controller import UploadUsersController
# from .upload_users_usecase import UploadUsersUsecase
from src.shared.helpers.external_interfaces.http_lambda_requests import LambdaHttpRequest, LambdaHttpResponse
from src.shared.environments import Environments

repo = Environments.get_user_repo()()
# usecase = UploadUsersUsecase(repo)
# controller = UploadUsersController(usecase)


def lambda_handler(event, context):
    
    print(event)