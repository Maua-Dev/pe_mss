from typing import Optional, Union
from src.shared.domain.entities.user import User
from src.shared.domain.enums.active_enum import ACTIVE
from src.shared.domain.enums.course_enum import COURSE
from src.shared.domain.enums.organization_enum import ORGANIZATION
from src.shared.domain.enums.role_enum import ROLE
from src.shared.domain.enums.state_enum import STATE
from src.shared.domain.repositories.user_repository_interface import IUserRepository
from src.shared.environments import Environments
from src.shared.helpers.errors.usecase_errors import ForbiddenAction, NoItemsFound
from src.shared.infra.dto.user_postgres_dto import UserPostgresDTO
from src.shared.infra.external.postgres.datasources.postgres_datasource import RdsDataDatasource, RdsDataError
from src.shared.infra.external.postgres.datasources.postgres_datasource_tests import TestsRdsDatasource
from src.shared.helpers.errors.usecase_errors import DuplicatedItem
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

class UserRepositoryPostgres(IUserRepository):
    def __init__(self, db_datasource: RdsDataDatasource | TestsRdsDatasource):
        self.postgres = db_datasource

    def create_user(self, new_user: User) -> User | None:
        """
        Cria um novo usuário no banco de dados dentro de uma transação segura.

        Args:
            new_user (User): A entidade de usuário a ser criada.

        Returns:
            User | None: A entidade do usuário criado com os dados retornados 
                         do banco, ou None se a criação falhar.
        """
        query = """
            INSERT INTO users (user_id, name, email, ra, role, state, active, course, year, organization)
            VALUES (:user_id, :name, :email, :ra, :role, :state, :active, :course, :year, :organization)
            RETURNING *;
        """
        
        user_dto = UserPostgresDTO.from_entity(new_user).to_postgres()

        try:
            with self.postgres.transaction() as tx_id:
                result = self.postgres.query(
                    sql=query,
                    params=user_dto, 
                    transaction_id=tx_id
                )

                if result:
                    user_data_from_db = result[0]
                    return UserPostgresDTO.from_postgres(user_data_from_db).to_entity()

            raise Exception("Erro ao criar usuário.")

        except RdsDataError as e:

            if "duplicate key value violates unique constraint" in str(e):

                raise DuplicatedItem("email, id or ra")

            raise Exception("Erro ao criar usuário.")
    
    def delete_user(self, user_id: str) -> User:
        query = """
            DELETE FROM users WHERE user_id = :user_id
            RETURNING *;
        """
        params = {"user_id": user_id}

        try:
            with self.postgres.transaction() as tx_id:
                result = self.postgres.query(
                    sql=query, 
                    params=params, 
                    transaction_id=tx_id
                )
            
            if result:
                user_data_from_db = result[0]
                return UserPostgresDTO.from_postgres(user_data_from_db).to_entity()
            
            raise NoItemsFound("There is no user with that user id")

        except RdsDataError as e:
            logger.error(f"Falha na transação ao deletar usuário {user_id}: {e}")
            raise
    

    def get_all_user(self):
        query= """
            SELECT * FROM users
        """
        result= self.postgres.query(sql=query)

        if result:
            users_list= []
            for user_data in result:
                users_list.append(UserPostgresDTO.from_postgres(user_data).to_entity())
            return users_list
            
        raise NoItemsFound("There is no user in the database")
    
    # Essas funções foram comentadas pois o filtro é feito na camada de usecase, mas podem ser utilizadas futuramente
    # caso o processamento precise ser feito na camada de repositório por algum motivo de performance
    # def get_all_users_by_organization(self, organization: ORGANIZATION):
    #     query= """
    #         SELECT * FROM users WHERE organization = :organization
    #     """
    #     params= {"organization": organization.value}
    #     result= self.postgres.query(sql=query, params=params)

    #     if result:
    #         users_list= []
    #         for user_data in result:
    #             users_list.append(UserPostgresDTO.from_postgres(user_data).to_entity())
    #         return users_list
            
    #     raise NoItemsFound(f"There is no user in the database with that organization {organization.name}")
    
    # def get_all_users_by_state(self, state: STATE):
    #     query= """
    #         SELECT * FROM users WHERE state = :state
    #     """
    #     params= {"state": state.value}
    #     result= self.postgres.query(sql=query, params=params)

    #     if result:
    #         users_list= []
    #         for user_data in result:
    #             users_list.append(UserPostgresDTO.from_postgres(user_data).to_entity())
    #         return users_list
            
    #     raise NoItemsFound(f"There is no user in the database with that state {state.name}")

    def get_user(self, user_id: str) -> User | None:
        query = """
            SELECT * FROM users WHERE user_id = :user_id
        """
        params = {"user_id": user_id}
        result = self.postgres.query(sql=query, params=params)

        if result:
            user_data_from_db = result[0]
            return UserPostgresDTO.from_postgres(user_data_from_db).to_entity()
            # return User.from_dict(user_data_from_db)

        return None

    def get_users(self,
                  name: Optional[str] = None,
                  ra: Optional[str] = None,
                  state: Optional[STATE] = None,
                  role: Optional[ROLE] = None,
                  active: Optional[ACTIVE] = None,
                  course: Optional[COURSE] = None,
                  year: Optional[int] = None,
                  organization: Optional[ORGANIZATION] = None
                  ):
        base_query= "SELECT * FROM users"
        conditions = []
        params = {}

        if name is not None:
            conditions.append("name = :name")
            params["name"] = name

        if ra is not None:
            conditions.append("ra = :ra")
            params["ra"] = ra
        
        if state is not None:
            conditions.append("state = :state")
            params["state"] = state.value
        
        if role is not None:
            conditions.append("role = :role")
            params["role"] = role.value

        if active is not None:
            conditions.append("active = :active")
            params["active"] = active.value

        if course is not None:
            conditions.append("course = :course")
            params["course"] = course.value
        
        if year is not None:
            conditions.append("year = :year")
            params["year"] = year
        
        if organization is not None:
            conditions.append("organization = :organization")
            params["organization"] = organization.value

        if conditions:
            where_clause = " WHERE " + " AND ".join(conditions)
            query = base_query + where_clause
        else:
            query = base_query

        result = self.postgres.query(sql=query, params=params if params else None)

        if not result:
            return []
        
        users_list= []
        for user_data in result:
            users_list.append(UserPostgresDTO.from_postgres(user_data).to_entity())

        return users_list
    def get_user_by_email(self, email: str) -> User | None:
        query = """
            SELECT * FROM users WHERE email = :email
        """
        params = {"email": email}
        result = self.postgres.query(sql=query, params=params)

        if result:
            user_data_from_db = result[0]
            return UserPostgresDTO.from_postgres(user_data_from_db).to_entity()
            # return User.from_dict(user_data_from_db)

        return None
        
    def has_permission_target_user(self, requester_id: str, target_user: User) -> Optional[bool]:
        if requester_id == target_user.user_id:
                return True
        
        query= """
            SELECT *
            FROM users WHERE user_id = :user_id
        """

        params_requester= {"user_id": requester_id}

        # pega o requester user
        result_requester = self.postgres.query(sql=query, params=params_requester)

        if result_requester:
            user_requester_data_from_db = result_requester[0]
            requester_user= UserPostgresDTO.from_postgres(user_requester_data_from_db).to_entity()
        else:
            raise NoItemsFound("No user was found with that requester id")
        
        if requester_user.active != ACTIVE.ACTIVE:
            raise ForbiddenAction("The requester user is not active")

        # caso seja adm, pode fazer qlqr coisa
        if requester_user.role == ROLE.ADM:
            return True

        # usuários comuns nao podem fazer ações (temporario)
        if requester_user.role == ROLE.USER:
            raise ForbiddenAction("Common user is not allowed to perform actions in other entities")

        # presidentes podem agir apenas sobre usuários!
        if target_user.role != ROLE.USER:
            raise ForbiddenAction("President is not allowed to perform actions in other presidents")

        # presidente só pode agir sobre a mesma organização
        if requester_user.organization != target_user.organization:
            raise ForbiddenAction("President is not allowed to perform action in other organization besides he's")

        return True

    def has_permission_target_id(self, requester_id: str, target_id: str) -> Optional[bool]:
        if requester_id == target_id:
                return True
        
        query= """
            SELECT *
            FROM users WHERE user_id = :user_id
        """

        params_requester= {"user_id": requester_id}
        params_target= {"user_id": target_id}

        # pega o requester user
        result_requester = self.postgres.query(sql=query, params=params_requester)

        if result_requester:
            user_requester_data_from_db = result_requester[0]
            requester_user= UserPostgresDTO.from_postgres(user_requester_data_from_db).to_entity()
        else:
            raise NoItemsFound("No user was found with that requester id")

        # pega o target user
        result_target = self.postgres.query(sql=query, params=params_target)

        if result_target:
            user_target_data_from_db = result_target[0]
            target_user= UserPostgresDTO.from_postgres(user_target_data_from_db).to_entity()
        else:
            raise NoItemsFound("No user was found with that target id")


        if requester_user.active != ACTIVE.ACTIVE:
            raise ForbiddenAction("The requester user is not active")
        
        # caso seja adm, pode fazer qlqr coisa
        if requester_user.role == ROLE.ADM:
            return True
        
        # usuários comuns nao podem fazer ações (temporario)
        if requester_user.role == ROLE.USER:
            raise ForbiddenAction("Common user is not allowed to perform actions in other entities")
        
         # presidentes podem agir apenas sobre usuários!
        if target_user.role != ROLE.USER:
            raise ForbiddenAction("President is not allowed to perform actions in other presidents")

        # presidente só pode agir sobre a mesma organização
        if requester_user.organization != target_user.organization:
            raise ForbiddenAction("President is not allowed to perform action in other organization besides he's")
        
        return True   

    def update_user(
        self, 
        user_id: str, 
        new_state: STATE=None, 
        new_role: ROLE=None, 
        new_active: ACTIVE=None, 
        new_course: COURSE=None, 
        new_year: int=None,  
        new_organization: ORGANIZATION=None
    ) -> User:
        query= """
            UPDATE users 
            SET 
                active= COALESCE(:new_active, active),
                state= COALESCE(:new_state, state),
                role= COALESCE(:new_role, role),
                course= COALESCE(:new_course, course),
                year= COALESCE(:new_year, year),
                organization= COALESCE(:new_organization, organization)
            WHERE user_id = :user_id
            RETURNING *
        """

        params= {
            "user_id": user_id,
            "new_active": new_active.value if new_active is not None else None,
            "new_state": new_state.value if new_state is not None else None,
            "new_role": new_role.value if new_role is not None else None,
            "new_course": new_course.value if new_course is not None else None,
            "new_year": new_year,
            "new_organization": new_organization.value if new_organization is not None else None
        }

        try:
            with self.postgres.transaction() as tx_id:
                result = self.postgres.query(
                    sql=query, 
                    params=params,
                    transaction_id=tx_id
                )

            if result:
                user_data_from_db = result[0]
                return UserPostgresDTO.from_postgres(user_data_from_db).to_entity()
                
            raise NoItemsFound("No user was found with that user id")

        except RdsDataError as e:
            logger.error(f"Falha na transação ao atualizar usuário {user_id}: {e}")
            raise
        
    def reallocate_id(self, user_id: str, email: str) -> User:
        query= """
            UPDATE users 
            SET 
                user_id= :new_user_id
            WHERE email = :email
            RETURNING *
        """

        params= {
            "new_user_id": user_id,
            "email": email
        }

        try:
            with self.postgres.transaction() as tx_id:
                result = self.postgres.query(
                    sql=query, 
                    params=params,
                    transaction_id=tx_id
                )

            if result:
                user_data_from_db = result[0]
                return UserPostgresDTO.from_postgres(user_data_from_db).to_entity()
                
            raise NoItemsFound("No user was found with that email")

        except RdsDataError as e:
            logger.error(f"Falha na transação ao realocar ID do usuário com email {email}: {e}")
            raise

    