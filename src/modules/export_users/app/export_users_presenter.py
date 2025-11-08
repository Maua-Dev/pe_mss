from .export_users_extractor import DownloadUsersExtractor
from .export_users_transformer import DownloadUsersTransformer
from src.shared.environments import Environments
from src.shared.helpers.external_interfaces.http_lambda_requests import LambdaHttpRequest, LambdaHttpResponse
import json


user_repo= Environments.get_user_repo()

def lambda_handler(event, context):   
    
    httpRequest = LambdaHttpRequest(data=event)

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

    print("Decoded user:", user_info)

    extractor= DownloadUsersExtractor(repo=user_repo)
    transformer= DownloadUsersTransformer(extractor=extractor)

    download=transformer()

    httpResponse= LambdaHttpResponse( 
        status_code= 200,
        body= download
    )

    return httpResponse.toDict()

    