import json

from src.modules.auth_user.app.auth_user_presenter import lambda_handler



class Test_AuthUserPresenter:
    
    def test_auth_user_and_user_is_in_repo_mock(self):
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
                    "iam": {
                        "accessKey": "AKIA...",
                        "accountId": "111122223333",
                        "callerId": "AIDA...",
                        "cognitoIdentity": None,
                        "principalOrgId": None,
                        "userArn": "arn:aws:iam::111122223333:user/example-user",
                        "userId": "AIDA..."
                    }
                },
                "domainName": "<url-id>.lambda-url.us-west-2.on.aws",
                "domainPrefix": "<url-id>",
                "external_interfaces": {
                    "method": "GET",
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
            "body": '{"user_id": "550e8400-e29b-41d4-a716-446655440000", "displayName": "Guilherme", "email": "25.00178-5@maua.br"}',
            "pathParameters": None,
            "isBase64Encoded": None,
            "stageVariables": None
        }

        response = lambda_handler(event, None)


        assert response["statusCode"] == 200
        assert json.loads(response["body"])['displayName'] == 'Guilherme'
        assert json.loads(response["body"])['email'] == '25.00178-5@maua.br'
        assert json.loads(response["body"])['ra'] == '25.00178-5'
        assert json.loads(response["body"])['state'] == 'PENDING'
        assert json.loads(response["body"])['role'] == 'USER'
        assert json.loads(response["body"])['message'] == 'the user was retrieved successfully'
