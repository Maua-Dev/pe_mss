from src.shared.domain.entities.user import User
from src.shared.domain.repositories.user_repository_interface import IUserRepository
from src.shared.environments import Environments
from src.shared.infra.external.postgres.datasources.postgres_datasource import RdsDataDatasource


class UserRepositoryPostgres(IUserRepository):
    def __init__(self, db_datasource):
        self.postgres = db_datasource

    def create_user(self, new_user: User) -> User | None:
        query = """
            INSERT INTO users (user_id, name, email, ra, role, state, active, course, year, organization)
            VALUES (:user_id, :name, :email, :ra, :role, :state, :active, :course, :year, :organization)
            RETURNING *;
        """
        
        params = {
            "user_id": new_user.user_id,
            "name": new_user.name,
            "email": new_user.email,
            "ra": new_user.ra,
            "role": new_user.role.value if new_user.role else None,
            "state": new_user.state.value if new_user.state else None,
            "active": new_user.active.value if new_user.active else None,
            "course": new_user.course.value if new_user.course else None,
            "year": new_user.year,
            "organization": new_user.organization.value if new_user.organization else None
        }
        
        result = self.postgres.query(sql=query, params=params)

        if result:
            user_data_from_db = result[0]
            return User.from_dict(user_data_from_db)
            
        return None
    
    def delete_user(self, user_id: str) -> bool:
        query = """
            DELETE FROM users WHERE user_id = :user_id
        """
        params = {"user_id": user_id}
        result = self.postgres.query(sql=query, params=params)
        return result is not None

    def get_all_user(self, *args, **kwargs):
        raise NotImplementedError

    def get_user(self, *args, **kwargs):
        raise NotImplementedError

    def has_permission_target_id(self, *args, **kwargs):
        raise NotImplementedError

    def has_permission_target_user(self, *args, **kwargs):
        raise NotImplementedError

    def update_user(self, *args, **kwargs):
        raise NotImplementedError
    