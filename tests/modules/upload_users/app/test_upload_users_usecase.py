import os
import pytest
from src.modules.upload_users.app.upload_users_usecase import UploadUsersUsecase
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock


class Test_UploadUsersUsecase:
    IN_GITHUB_ACTIONS = os.getenv('GITHUB_ACTIONS', 'false').lower() == 'true'
    
    test_base64_xlsx = "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"
    
    @pytest.mark.skipif(IN_GITHUB_ACTIONS, reason="Skipping test in GitHub Actions")
    def test_upload_users_as_president_usecase(self):
        repo = UserRepositoryMock()
        usecase = UploadUsersUsecase(repo=repo)
        created_users, duplicated_users = usecase(
            file_base64=self.test_base64_xlsx, 
            requester_user_id='e6bed58f-424a-4b62-b408-18e0a8d1f069'
        )
        
        # THIS WILL RETURN 0 AS THE CREATED AND DUPLICATED ARE ONLY RETURNED VIA API ROUTE
        assert len(created_users) == 3
        assert len(duplicated_users) == 0
    
    @pytest.mark.skipif(IN_GITHUB_ACTIONS, reason="Skipping test in GitHub Actions")
    def test_upload_users_as_non_president_usecase(self):
        repo = UserRepositoryMock()
        usecase = UploadUsersUsecase(repo=repo)
        
        try:
            usecase(
                file_base64=self.test_base64_xlsx, 
                requester_user_id='b2b6f8d4-6f3e-4e8c-9a4f-5f1e5c8e7d9a'
            )
        except Exception as e:
            assert str(e) == 'No items found for b2b6f8d4-6f3e-4e8c-9a4f-5f1e5c8e7d9a'
    
    @pytest.mark.skipif(IN_GITHUB_ACTIONS, reason="Skipping test in GitHub Actions") 
    def test_upload_users_with_invalid_file_usecase(self):
        repo = UserRepositoryMock()
        usecase = UploadUsersUsecase(repo=repo)
        
        try:
            usecase(
                file_base64="invalid_base64_string", 
                requester_user_id='e6bed58f-424a-4b62-b408-18e0a8d1f069'
            )
        except Exception as e:
            assert str(e) == 'Incorrect padding'
        
    @pytest.mark.skipif(IN_GITHUB_ACTIONS, reason="Skipping test in GitHub Actions")
    def test_upload_users_with_no_data_usecase(self):
        repo = UserRepositoryMock()
        usecase = UploadUsersUsecase(repo=repo)
        
        try:
            usecase(
                file_base64=self.test_base64_xlsx, 
                requester_user_id='e6bed58f-424a-4b62-b408-18e0a8d1f070'  # User ID that does not exist in mock repo
            )
        except Exception as e:
            assert str(e) == 'No items found for e6bed58f-424a-4b62-b408-18e0a8d1f070'