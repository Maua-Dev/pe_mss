from src.shared.domain.entities.user import User
from src.shared.domain.enums.state_enum import STATE


class UploadUsersViewmodel:
    status: int

    def __init__(self, status: int):
        self.status = status

    def to_dict(self):
        return {
            'status': self.status,
            'message': "the users were uploaded successfully" if self.status == 200 else "there was an error uploading the users"
        }

