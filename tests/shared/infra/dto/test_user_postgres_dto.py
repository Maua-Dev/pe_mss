from src.shared.domain.entities.user import User
from src.shared.domain.enums.active_enum import ACTIVE
from src.shared.domain.enums.course_enum import COURSE
from src.shared.domain.enums.organization_enum import ORGANIZATION
from src.shared.domain.enums.role_enum import ROLE
from src.shared.domain.enums.state_enum import STATE
from src.shared.infra.dto.user_postgres_dto import UserPostgresDTO
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock


class Test_UserPostgresDTO:
    def test_from_entity(self):
        repo= UserRepositoryMock()

        user_dto= UserPostgresDTO.from_entity(user=repo.users[0])

        expected_selfie_dto = UserPostgresDTO(
            user_id=repo.users[0].user_id,
            name=repo.users[0].name,
            email=repo.users[0].email,
            ra=repo.users[0].ra,
            state=repo.users[0].state,
            course=repo.users[0].course,
            year=repo.users[0].year,
            role=repo.users[0].role,
            active=repo.users[0].active,
            organization=repo.users[0].organization
        )

        assert user_dto == expected_selfie_dto


    def test_to_postgres(self):
        repo= UserRepositoryMock()

        user_dto= UserPostgresDTO(
            user_id=repo.users[0].user_id,
            name=repo.users[0].name,
            email=repo.users[0].email,
            ra=repo.users[0].ra,
            role=repo.users[0].role,
            state=repo.users[0].state,
            active=repo.users[0].active,
            course=repo.users[0].course,
            year=repo.users[0].year,
            organization=repo.users[0].organization
        )

        user_postgres= user_dto.to_postgres()

        expected_dict= {
            "user_id": repo.users[0].user_id,
            "name": repo.users[0].name,
            "email": repo.users[0].email,
            "ra": repo.users[0].ra if repo.users[0].ra else None,
            "role": repo.users[0].role.value,
            "state": repo.users[0].state.value,
            "active": repo.users[0].active.value,
            "course": repo.users[0].course.value if repo.users[0].course else None,
            "year": repo.users[0].year if repo.users[0].year else None,
            "organization": repo.users[0].organization if repo.users[0].organization else None
        }

        assert user_postgres == expected_dict


    def test_from_postgres(self): 
        postgres_dict= {
            'user_data': {
                'user_id': '550e8400-e29b-41d4-a716-446655440000',
                'name': 'Guilherme',
                'email': '25.00178-5@maua.br',
                'ra': '25.00178-5',
                'role': 'USER',
                'state': 'PENDING',
                'active': 'ACTIVE',
                'course': 'CIC',
                'year': 2,
                'organization': 'DEV'
            }
        }

        user_dto= UserPostgresDTO.from_postgres(user_data=postgres_dict['user_data'])

        expect_user_dto= UserPostgresDTO(
            user_id= '550e8400-e29b-41d4-a716-446655440000',
            name= 'Guilherme',
            email='25.00178-5@maua.br',
            ra= '25.00178-5',
            role='USER',
            state='PENDING',
            active= 'ACTIVE',
            course='CIC',
            year= 2,
            organization= 'DEV'
        )

    def test_to_entity(self):
        repo= UserRepositoryMock()

        user_dto= UserPostgresDTO(
            user_id=repo.users[0].user_id,
            name=repo.users[0].name,
            email=repo.users[0].email,
            ra=repo.users[0].ra,
            role=repo.users[0].role,
            state=repo.users[0].state,
            active=repo.users[0].active,
            course=repo.users[0].course,
            year=repo.users[0].year,
            organization=repo.users[0].organization
        )

        user_postgres= user_dto.to_entity()

        assert user_postgres.user_id == repo.users[0].user_id
        assert user_postgres.name == repo.users[0].name
        assert user_postgres.email == repo.users[0].email
        assert user_postgres.ra == repo.users[0].ra
        assert user_postgres.role == repo.users[0].role
        assert user_postgres.state == repo.users[0].state
        assert user_postgres.active == repo.users[0].active
        assert user_postgres.course == repo.users[0].course
        assert user_postgres.year == repo.users[0].year
        assert user_postgres.organization == repo.users[0].organization


    def test_from_postgres_to_entity(self):
        postgres_item= {
            'user_data': {
                'user_id': '550e8400-e29b-41d4-a716-446655440000',
                'name': 'Guilherme',
                'email': '25.00178-5@maua.br',
                'ra': '25.00178-5',
                'role': 'USER',
                'state': 'PENDING',
                'active': 'ACTIVE',
                'course': 'CIC',
                'year': 2,
                'organization': 'DEV'
            }
        }

        user_dto= UserPostgresDTO.from_postgres(user_data=postgres_item["user_data"])

        user= user_dto.to_entity()

        expected_user = User(
            user_id= '550e8400-e29b-41d4-a716-446655440000',
            name= 'Guilherme',
            email= '25.00178-5@maua.br',
            ra= '25.00178-5',
            role= ROLE.USER,
            state= STATE.PENDING,
            active= ACTIVE.ACTIVE,
            course= COURSE.CIC,
            year= 2,
            organization= ORGANIZATION.DEV
        )

        assert user.user_id == expected_user.user_id
        assert user.name == expected_user.name
        assert user.email == expected_user.email
        assert user.ra == expected_user.ra
        assert user.role == expected_user.role
        assert user.state == expected_user.state
        assert user.active == expected_user.active
        assert user.course == expected_user.course
        assert user.year == expected_user.year
        assert user.organization == expected_user.organization

    def test_from_entity_to_postgres(self):
        repo= UserRepositoryMock()

        user_dto= UserPostgresDTO.from_entity(user=repo.users[0])

        user_postgres= user_dto.to_postgres()

        expect_dict= {
            'user_id': repo.users[0].user_id,
            'name': repo.users[0].name,
            'email': repo.users[0].email,
            'ra': repo.users[0].ra,
            'role': repo.users[0].role.value,
            'state': repo.users[0].state.value,
            'active': repo.users[0].active.value,
            'course': repo.users[0].course,
            'year': repo.users[0].year,
            'organization': repo.users[0].organization
        }

        assert user_postgres == expect_dict