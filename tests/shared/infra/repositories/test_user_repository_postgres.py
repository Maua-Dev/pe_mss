
from unittest.mock import MagicMock
import pytest
from src.shared.domain.entities.user import User
from src.shared.domain.enums.active_enum import ACTIVE
from src.shared.domain.enums.course_enum import COURSE
from src.shared.domain.enums.organization_enum import ORGANIZATION
from src.shared.domain.enums.role_enum import ROLE
from src.shared.domain.enums.state_enum import STATE
from src.shared.infra.external.postgres.datasources.postgre_tests_datasource import PostgresTestDatasource
from src.shared.infra.external.postgres.datasources.postgres_datasource import RdsDataDatasource
from src.shared.infra.repositories.user_repository_postgres import UserRepositoryPostgres


class TestUserRepositoryPostgres:

    def test_create_user(self):
        mock_datasource = MagicMock(spec=RdsDataDatasource)

        new_user = User(
            user_id="a1b2c3d4-e5f6-7890-1234-567890abcdef",
            name="Murillo Strina",
            email="22.00730-0@maua.br",
            ra="22.00730-0",
            role=ROLE.USER,
            state=STATE.PENDING,
            active=ACTIVE.ACTIVE,
            course=COURSE.ECM,
            year=4,
            organization=ORGANIZATION.NAWAT
        )

        mock_datasource.query.return_value = [new_user.to_dict()]

        repo = UserRepositoryPostgres(db_datasource=mock_datasource)

        response_user = repo.create_user(new_user)

        assert response_user is not None
        assert response_user.user_id == new_user.user_id
        assert response_user.name == "Murillo Strina"

        expected_sql = """
            INSERT INTO users (user_id, name, email, ra, role, state, active, course, year, organization)
            VALUES (:user_id, :name, :email, :ra, :role, :state, :active, :course, :year, :organization)
            RETURNING *;
        """
        
        expected_params = {
            "user_id": new_user.user_id,
            "name": new_user.name,
            "email": new_user.email,
            "ra": new_user.ra,
            "role": new_user.role.value,
            "state": new_user.state.value,
            "active": new_user.active.value,
            "course": new_user.course.value,
            "year": new_user.year,
            "organization": new_user.organization.value
        }

        mock_datasource.query.assert_called_once_with(sql=expected_sql, params=expected_params)