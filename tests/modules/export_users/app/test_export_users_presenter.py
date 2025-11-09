
from src.shared.helpers.external_interfaces.http_lambda_requests import LambdaHttpRequest
from src.modules.export_users.app.export_users_presenter import lambda_handler
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock


class TestExportUsersPresenter:
    
    def test_export_users_presenter(self):
        
        user_repo= UserRepositoryMock()
        
        event = {
            "version": "2.0",
            "routeKey": "$default",
            "rawPath": "/my/path",
            "rawQueryString": "parameter1=value1&parameter1=value2&parameter2=value",
            "cookies": [
                "cookie1",
                "cookie2"
            ],
            "headers": {
                "header1": "value1",
                "header2": "value1,value2"
            },
            "queryStringParameters": {
                "parameter1": "1"
            },
            "requestContext": {
                "accountId": "123456789012",
                "apiId": "<urlid>",
                "authentication": None,
                "authorizer": {
                    "user": {
                        "id": user_repo.users[1].user_id,
                        "displayName": "João", 
                        "mail": "21.00678-2@maua.br"
                    }
                },
                "domainName": "<url-id>.lambda-url.us-west-2.on.aws",
                "domainPrefix": "<url-id>",
                "external_interfaces": {
                    "method": "POST",
                    "path": "/my/path",
                    "protocol": "HTTP/1.1",
                    "sourceIp": "123.123.123.123",
                    "userAgent": "agent"
                },
                "requestId": "id",
                "routeKey": "$default",
                "stage": "$default",
                "time": "12/Mar/2020:19:03:58 +0000",
                "timeEpoch": 1583348638390
            },
            "body": '',
            "pathParameters": None,
            "isBase64Encoded": None,
            "stageVariables": None
        }

        response = lambda_handler(event=event, context= None)

        assert response["statusCode"] == 200