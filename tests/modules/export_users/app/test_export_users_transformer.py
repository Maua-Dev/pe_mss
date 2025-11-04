import base64
import os
import sys
import subprocess
import tempfile

import pytest
from src.modules.export_users.app.export_users_extractor import DownloadUsersExtractor
from src.modules.export_users.app.export_users_transformer import DownloadUsersTransformer
from src.shared.infra.external.postgres.datasources.postgres_datasource_tests import TestsRdsDatasource
from src.shared.infra.repositories.user_repository_postgres import UserRepositoryPostgres


class TestDownloadUsers:
    IN_GITHUB_ACTIONS = os.getenv('GITHUB_ACTIONS', 'false').lower() == 'true'
    
    @pytest.mark.skipif(IN_GITHUB_ACTIONS, reason="Skipping tests in GitHub Actions environment")
    def test_export_users_transformer(self):
        datasource= TestsRdsDatasource()
        
        user_repo= UserRepositoryPostgres(datasource)

        extractor= DownloadUsersExtractor(repo=user_repo)

        transformer= DownloadUsersTransformer(extractor=extractor)

        output_base64= transformer()

        output= base64.b64decode(output_base64)

        with tempfile.NamedTemporaryFile(delete=False, suffix = ".xlsx") as temp_file:
            temp_file.write(output)
            temp_file_path = temp_file.name


        if sys.platform.startswith("darwin"):  # macOS
            subprocess.call(["open", temp_file_path])

        elif sys.platform.startswith("linux"):
            subprocess.call(["xdg-open", temp_file_path])
            
        elif sys.platform.startswith("win"):
            os.startfile(temp_file_path)
