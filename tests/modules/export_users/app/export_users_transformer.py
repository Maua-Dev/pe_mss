import base64
import os
import tempfile

import pytest
from src.modules.export_users.app.export_users_extractor import DownloadUsersExtractor
from src.modules.export_users.app.export_users_transformer import DownloadUsersTransformer
from src.shared.infra.repositories.user_repository_postgres import UserRepositoryPostgres


class TestDownloadUsersTransformer:
    @pytest.mark.skip("Can't run test in gh actions")
    def test_download_users_transformer(self):

        user_repo= UserRepositoryPostgres()

        extractor= DownloadUsersExtractor(repo=user_repo)

        transformer= DownloadUsersTransformer(extractor=extractor)

        output_base64= transformer()

        output= base64.b64decode(output_base64)

        with tempfile.NamedTemporaryFile(delete=False, suffix = ".xlsx") as temp_file:
            temp_file.write(output.read())
            temp_file_path = temp_file.name

        os.startfile(temp_file_path)
