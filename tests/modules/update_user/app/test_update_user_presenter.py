import json
from src.modules.update_user.app.update_user_presenter import lambda_handler

class TestUpdateUserPresenter:

    def test_update_user_fail(self):
        event = {
            "version": "2.0",
            "routeKey": "$default",
            "rawPath": "/update_user",
            "rawQueryString": "",
            "headers": {"Content-Type": "application/json"},
            "requestContext": {
                "authorizer": {
                    "user": {
                        "id": "550e8400-e29b-41d4-a716-446655440000",
                        "displayName": "Guilherme",
                        "mail": "25.00178-5@maua.br"
                    }
                }
            },
            "body": json.dumps({
                "user_id": "1",
                "name": "Novo Nome do Usuário"
            }),
            "isBase64Encoded": False
        }

        response = lambda_handler(event, None)
        body = response["body"]

        assert response["statusCode"] == 500

    def test_update_user_missing_user_id(self):
        event = {
            "version": "2.0",
            "routeKey": "$default",
            "rawPath": "/update_user",
            "rawQueryString": "",
            "headers": {"Content-Type": "application/json"},
            "requestContext": {
                "authorizer": {
                    "user": {
                        "id": "550e8400-e29b-41d4-a716-446655440000",
                        "displayName": "Guilherme",
                        "mail": "25.00178-5@maua.br"
                    }
                }
            },
            "body": json.dumps({
                "name": "Outro Nome"
            }),
            "isBase64Encoded": False
        }

        response = lambda_handler(event, None)
        body = response["body"]

        assert response["statusCode"] == 400
        assert body.strip('"') == "Field user_id is missing"  # mensagem real do presenter

    def test_update_user_missing_new_name(self):
        event = {
            "version": "2.0",
            "routeKey": "$default",
            "rawPath": "/update_user",
            "rawQueryString": "",
            "headers": {"Content-Type": "application/json"},
            "requestContext": {
                "authorizer": {
                    "user": {
                        "id": "550e8400-e29b-41d4-a716-446655440000",
                        "displayName": "Guilherme",
                        "mail": "25.00178-5@maua.br"
                    }
                }
            },
            "body": json.dumps({
                "user_id": "1"
            }),
            "isBase64Encoded": False
        }

        response = lambda_handler(event, None)
        body = response["body"]

        assert response["statusCode"] == 500
        assert body.strip('"') == "Invalid format for user id"

    def test_update_user_not_found(self):
        event = {
            "version": "2.0",
            "routeKey": "$default",
            "rawPath": "/update_user",
            "rawQueryString": "",
            "headers": {"Content-Type": "application/json"},
            "requestContext": {
                "authorizer": {
                    "user": {
                        "id": "550e8400-e29b-41d4-a716-446655440000",
                        "displayName": "Guilherme",
                        "mail": "25.00178-5@maua.br"
                    }
                }
            },
            "body": json.dumps({
                "user_id": "550e8411-e29b-41d4-a716-446655440000",
                "name": "Nome Inexistente"
            }),
            "isBase64Encoded": False
        }

        response = lambda_handler(event, None)
        body = response["body"]

        assert response["statusCode"] == 404
