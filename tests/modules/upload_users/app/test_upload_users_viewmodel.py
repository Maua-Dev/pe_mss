from src.modules.upload_users.app.upload_users_viewmodel import UploadUsersViewmodel


class Test_UploadUsersViewmodel:
    def test_upload_users_viewmodel(self):
        viewmodel = UploadUsersViewmodel(
            status=200,
            uploaded_users=[{'user_id': '1', 'name': 'User One'}],
            duplicated_users=[{'user_id': '2', 'name': 'User Two'}]
        )
        
        assert viewmodel.status == 200
        assert viewmodel.to_dict() == {
            'status': 200, 
            'operation_for_comparison': {
                'uploaded_users': [{'user_id': '1', 'name': 'User One'}],
                'duplicated_users': [{'user_id': '2', 'name': 'User Two'}]
            },
            'message': "the users were uploaded successfully"
        }