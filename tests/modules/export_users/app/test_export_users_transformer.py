import base64
import os
import sys
import subprocess
import tempfile

import pytest
from src.modules.export_users.app.export_users_extractor import DownloadUsersExtractor
from src.modules.export_users.app.export_users_transformer import DownloadUsersTransformer
from src.shared.helpers.external_interfaces.http_lambda_requests import LambdaHttpRequest
from src.shared.helpers.external_interfaces.http_models import HttpRequest
from src.shared.infra.external.postgres.datasources.postgres_datasource_tests import TestsRdsDatasource
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock
from src.shared.infra.repositories.user_repository_postgres import UserRepositoryPostgres


class TestDownloadUsers:
    IN_GITHUB_ACTIONS = os.getenv('GITHUB_ACTIONS', 'false').lower() == 'true'
    
    def test_export_users_transformer(self):
        
        user_repo= UserRepositoryMock()

        extractor= DownloadUsersExtractor(repo=user_repo)

        transformer= DownloadUsersTransformer(extractor=extractor)
        
        request = HttpRequest(body={
            'user_from_authorizer':{
                'id': user_repo.users[1].user_id,
                'displayName': user_repo.users[1].name,
                'mail': user_repo.users[1].email
            }
        })

        response = transformer(request=request)

        output= base64.b64decode(response.body['file_base64'])

        with tempfile.NamedTemporaryFile(delete=False, suffix = ".xlsx") as temp_file:
            temp_file.write(output)
            temp_file_path = temp_file.name


        if sys.platform.startswith("darwin"):  # macOS
            subprocess.call(["open", temp_file_path])

        elif sys.platform.startswith("linux"):
            subprocess.call(["xdg-open", temp_file_path])
            
        elif sys.platform.startswith("win"):
            os.startfile(temp_file_path)
            
    def test_export_users_transformer_forbidden(self):
        
        user_repo= UserRepositoryMock()

        extractor= DownloadUsersExtractor(repo=user_repo)

        transformer= DownloadUsersTransformer(extractor=extractor)
        
        request = HttpRequest(body={
            'user_from_authorizer':{
                'id': user_repo.users[0].user_id,
                'displayName': user_repo.users[0].name,
                'mail': user_repo.users[0].email
            }
        })

        response = transformer(request=request)

        assert response.status_code == 403
            
    @pytest.mark.skipif(IN_GITHUB_ACTIONS, reason="Skipping tests in GitHub Actions environment")
    def test_export_users_transformer_real_repo(self):
                    
        datasource= TestsRdsDatasource()
                    
        user_repo= UserRepositoryPostgres(db_datasource=datasource)

        extractor= DownloadUsersExtractor(repo=user_repo)

        transformer= DownloadUsersTransformer(extractor=extractor)
        
        request = HttpRequest(body={
            'user_from_authorizer':{
                'id': '550e8400-e29b-41d4-a716-446655440001',
                'displayName': 'Admin User',
                'mail': 'admin@example.com'
            }
        })
        
        response = transformer(request=request)
        
        assert response.status_code == 200
        
        output= base64.b64decode(response.body['file_base64'])

        with tempfile.NamedTemporaryFile(delete=False, suffix = ".xlsx") as temp_file:
            temp_file.write(output)
            temp_file_path = temp_file.name


        if sys.platform.startswith("darwin"):  # macOS
            subprocess.call(["open", temp_file_path])

        elif sys.platform.startswith("linux"):
            subprocess.call(["xdg-open", temp_file_path])
            
        elif sys.platform.startswith("win"):
            os.startfile(temp_file_path)
