from src.shared.domain.entities.user import User
from src.shared.domain.enums.state_enum import STATE


class UploadUsersViewmodel:
    status: int
    uploaded_users: list[dict]
    duplicated_users: list[dict]

    def __init__(self, status: int, uploaded_users: list[dict] = None, duplicated_users: list[dict] = None):
        self.status = status
        self.uploaded_users = uploaded_users if uploaded_users else []
        self.duplicated_users = duplicated_users if duplicated_users else []

    def to_dict(self):
        return {
            'status': self.status,
            'operation_for_comparison': {
                'uploaded_users': self.uploaded_users,
                'duplicated_users': self.duplicated_users
            },
            'message': "the users were uploaded successfully" if self.status == 200 else "there was an error uploading the users"
        }

