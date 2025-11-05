from src.modules.export_users.app.export_users_extractor import DownloadUsersExtractor
from src.modules.export_users.app.export_users_transformer import DownloadUsersTransformer
from src.shared.environments import Environments
from src.shared.helpers.external_interfaces.http_lambda_requests import LambdaHttpResponse


user_repo= Environments.get_user_repo()

def lambda_handler(event, context):   

    extractor= DownloadUsersExtractor(repo= user_repo)
    transformer= DownloadUsersTransformer(extractor= extractor)

    download= transformer()

    httpResponse= LambdaHttpResponse( 
        status_code= 200,
        body= download
    )

    return httpResponse.toDict()

    