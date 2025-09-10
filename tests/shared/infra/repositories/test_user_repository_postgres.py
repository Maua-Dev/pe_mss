
import pytest
from src.shared.domain.entities.user import User
from src.shared.domain.enums.active_enum import ACTIVE
from src.shared.domain.enums.course_enum import COURSE
from src.shared.domain.enums.organization_enum import ORGANIZATION
from src.shared.domain.enums.role_enum import ROLE
from src.shared.domain.enums.state_enum import STATE
from src.shared.infra.external.postgres.datasources.postgre_tests_datasource import PostgresTestDatasource
from src.shared.infra.repositories.user_repository_postgres import UserRepositoryPostgres


class TestUserRepositoryPostgres:
    
    @pytest.mark.skip(reason="Needs PostgreSQL")
    def test_create_user(self):
        datasource = PostgresTestDatasource()
        repo = UserRepositoryPostgres(db_datasource=datasource)
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

        resp = repo.create_user(new_user)

        assert resp == new_user