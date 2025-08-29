from src.shared.domain.entities.user import User
from src.shared.domain.enums.state_enum import STATE


class DeleteUserViewmodel:
    user_id: int

    def __init__(self, user: User):
        self.user_id = user.user_id

    def to_dict(self):
        return {
            'user_id': self.user_id,
            'message': "the user was deleted successfully"
        }

