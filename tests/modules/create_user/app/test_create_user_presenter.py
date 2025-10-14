import json
from src.modules.create_user.app.create_user_presenter import lambda_handler


class Test_CreateUserPresenter:

    def test_create_user_as_admin(self):
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
                        "id": "550e8400-e29b-41d4-a716-446655440001",
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
            "body": '{"new_user": {"name": "Maria", "email": "21.00100-2@maua.br", "organization": "DEV", "role": "USER"}}',
            "pathParameters": None,
            "isBase64Encoded": None,
            "stageVariables": None
        }

        response = lambda_handler(event, None)

        assert response["statusCode"] == 200
        assert json.loads(response["body"])['user_id'] is not None
        assert json.loads(response["body"])['name'] == "Maria"
        assert json.loads(response["body"])['email'] == "21.00100-2@maua.br"
        assert json.loads(response["body"])['organization'] == "DEV"
        assert json.loads(response["body"])['role'] == "USER"
        assert json.loads(response["body"])['active'] == "ACTIVE"
        assert json.loads(response["body"])['state'] == "PENDING"
        assert json.loads(response["body"])['ra'] == "21.00100-2"

    def test_create_user_presenter_without_user_from_authorizer(self):
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
                    "user": None
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
            "body": '{"new_user": {"name": "Maria", "email": "21.00100-2@maua.br", "organization": "DEV", "role": "USER"}}',
            "pathParameters": None,
            "isBase64Encoded": None,
            "stageVariables": None
        }

        response = lambda_handler(event, None)

        assert response["statusCode"] == 400
        assert json.loads(response["body"]) == "Field user_from_authorizer is missing"

    def test_create_user_presenter_without_new_user(self):
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
                        "id": "550e8400-e29b-41d4-a716-446655440001",
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

        response = lambda_handler(event, None)

        assert response["statusCode"] == 400
        assert json.loads(response["body"]) == "Field new_user is missing"

    def test_create_user_presenter_as_president(self):
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
                        "id": "550e8400-e29b-41d4-a716-446655440002",
                        "displayName": "Heitor", 
                        "mail": "21.00453-7@maua.br"
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
            "body": '{"new_user": {"name": "Maria", "email": "21.00100-4@maua.br", "organization": "NAWAT", "role": "USER", "course": "CIC", "year": 4}}',
            "pathParameters": None,
            "isBase64Encoded": None,
            "stageVariables": None
        } 
       
        response = lambda_handler(event, None)

        assert response["statusCode"] == 200
        assert json.loads(response["body"])['user_id'] is not None
        assert json.loads(response["body"])['name'] == "Maria"
        assert json.loads(response["body"])['email'] == "21.00100-4@maua.br"
        assert json.loads(response["body"])['organization'] == "NAWAT"
        assert json.loads(response["body"])['role'] == "USER"
        assert json.loads(response["body"])['active'] == "ACTIVE"
        assert json.loads(response["body"])['state'] == "PENDING"
        assert json.loads(response["body"])['ra'] == "21.00100-4"

    def test_create_user_presenter_as_unauthorized_president(self):
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
                        "id": "550e8400-e29b-41d4-a716-446655440002",
                        "displayName": "Heitor", 
                        "mail": "21.00453-7@maua.br"
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
            "body": '{"new_user": {"name": "Maria", "email": "21.00100-4@maua.br", "organization": "DEV", "role": "USER", "course": "CIC", "year": 4}}',
            "pathParameters": None,
            "isBase64Encoded": None,
            "stageVariables": None
        } 
       
        response = lambda_handler(event, None)

        assert response["statusCode"] == 403