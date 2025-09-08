from src.modules.auth_user.app.auth_user_viewmodel import AuthUserViewmodel
from src.shared.domain.entities.user import User
from src.shared.domain.enums.organization_enum import ORGANIZATION
from src.shared.domain.enums.role_enum import ROLE
from src.shared.domain.enums.state_enum import STATE
from src.shared.domain.enums.active_enum import ACTIVE


class Test_AuthUserViewmodel:
    def test_auht_user_viewmodel_user_is_in_repo_mock(self):
        user=User(
            user_id='550e8400-e29b-41d4-a716-446655440000',
            name="Guilherme",
            email="25.00178-5@maua.br", 
            state=STATE.PENDING, 
            role=ROLE.USER,
            organization= None,
            ra="25.00178-5",
            active=ACTIVE.ACTIVE
        )
        case_number= 0

        registerd_user= AuthUserViewmodel(user=user, case_number=case_number)

        expected= {
            'id': '550e8400-e29b-41d4-a716-446655440000',
            'displayName': 'Guilherme',
            'email': '25.00178-5@maua.br',
            'ra': '25.00178-5',
            'state': 'PENDING',
            'role': 'USER',
            'organization': None,
            'message': 'the user was retrieved successfully',
            'active': 'ACTIVE'
        }

        assert registerd_user.to_dict() == expected

    def test_auth_user_viewmodel_user_not_in_repo_mock(self):
        user= User(
            user_id= "550e8400-e29b-41d4-a716-446655440010",
            name= "José",
            email= "20.00158-5@maua.br", 
            state= STATE.PENDING, 
            role= ROLE.USER,
            organization= None,
            ra= "20.00158-5",
            active=ACTIVE.FREEZED
        )
        case_number= 1

        registerd_user= AuthUserViewmodel(user=user, case_number=case_number)

        expected= {
            'id' : '550e8400-e29b-41d4-a716-446655440010',
            'displayName': 'José',
            'email': '20.00158-5@maua.br',
            'ra': '20.00158-5',
            'state': 'PENDING',
            'role': 'USER',
            'organization': None,
            'message': 'the user was created successfully',
            'active': 'FREEZED'

        }

        assert registerd_user.to_dict() == expected


