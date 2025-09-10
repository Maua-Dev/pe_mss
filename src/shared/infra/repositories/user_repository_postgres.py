from src.shared.domain.entities.user import User
from src.shared.domain.repositories.user_repository_interface import IUserRepository
from src.shared.environments import Environments
from src.shared.infra.external.postgres.datasources.postgres_datasource import RdsDataDatasource


class UserRepositoryPostgres(IUserRepository):
    def __init__(self, db_datasource):
        self.postgres = db_datasource

    def create_user(self, new_user: User) -> User:
        query = """
            INSERT INTO users (user_id, name, email, role, state, active, course, year, organization)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING *;
        """
        params = (
            new_user.user_id,
            new_user.name,
            new_user.email,
            new_user.role.value if new_user.role else None,
            new_user.state.value if new_user.state else None,
            new_user.active.value if new_user.active else None,
            new_user.course.value if new_user.course else None,
            new_user.year,
            new_user.organization.value if new_user.organization else None
        )
        result = self.postgres.query(query=query, params=params)

        if result:
            return User(**result[0])
        return None