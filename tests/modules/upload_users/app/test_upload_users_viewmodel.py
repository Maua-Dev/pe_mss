from src.modules.upload_users.app.upload_users_viewmodel import UploadUsersViewmodel


class Test_UploadUsersViewmodel:
    def test_upload_users_viewmodel(self):
        viewmodel = UploadUsersViewmodel(status=200)
        
        assert viewmodel.status == 200
        assert viewmodel.to_dict() == {'status': 200, 'message': 'the users were uploaded successfully'}