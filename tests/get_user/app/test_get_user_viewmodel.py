from src.modules.get_all_users.app.get_all_users_viewmodel import GetUserViewModel
from src.modules.get_user.app.get_user_usecase import GetUserUsecase
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock


class TestUserViewModel:
    def test_get_user_viewmodel(self):
        user_repo = UserRepositoryMock()
        usecase = GetUserUsecase(user_repo=user_repo)
        user = usecase(user_id="550e8400-e29b-41d4-a716-446655440001")

        viewmodel = GetUserViewModel(user=user).to_dict()

        expected = {'user':{
            'user_id': '550e8400-e29b-41d4-a716-446655440001',
            'name': 'João',
            'email': '21.00678-2',
            'state': 'APPROVED',
            'role': 'ADM',
            'active': 'ACTIVE',
            'course': 'CIC',
            'year': 4,
            'organization': 'DEV'
        },
        'message': 'the user was retrieved'
        }  

        assert viewmodel == expected 