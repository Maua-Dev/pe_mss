from typing import List
from src.shared.domain.entities.user import User

from src.shared.domain.enums.active_enum import ACTIVE
from src.shared.domain.enums.state_enum import STATE
from src.shared.domain.repositories.user_repository_interface import IUserRepository
from src.shared.helpers.errors.usecase_errors import ForbiddenAction, NoItemsFound
from src.shared.domain.enums.course_enum import COURSE
from src.shared.domain.enums.organization_enum import ORGANIZATION
from src.shared.domain.enums.role_enum import ROLE
from typing import *
import uuid

class UserRepositoryMock(IUserRepository):
    users: List[User]
    
    def __init__(self):
        self.users = [
            User(
                name="Guilherme",
                email="25.00178-5@maua.br", 
                ra="25.00178-5", 
                state=STATE.PENDING, 
                role=ROLE.USER, 
                active=ACTIVE.ACTIVE, user_id="550e8400-e29b-41d4-a716-446655440000"),
            User(
                #adm tera organization?
                name="João",
                email="21.00678-2@maua.br", 
                ra="21.00678-2", 
                state=STATE.APPROVED, 
                role=ROLE.ADM,
                active=ACTIVE.ACTIVE, 
                course=COURSE.CIC, year=4, 
                organization=ORGANIZATION.DEV, user_id="550e8400-e29b-41d4-a716-446655440001"),
            User(
                #presidenete da nawat
                name="Heitor", 
                email="21.00453-7@maua.br", 
                ra="21.00453-7", 
                state=STATE.APPROVED, 
                role=ROLE.PRESIDENT, 
                active=ACTIVE.ACTIVE, 
                course=COURSE.ECM, 
                year=4, 
                organization=ORGANIZATION.NAWAT, user_id="550e8400-e29b-41d4-a716-446655440002"),
            User(
                #presidente da guardian
                name="Bruno", 
                email="21.00458-7@maua.br", 
                ra="21.00458-7", 
                state=STATE.REJECTED, 
                role=ROLE.PRESIDENT, 
                active=ACTIVE.DISCONNECTED, 
                course=COURSE.EET, 
                year=1, 
                organization=ORGANIZATION.GUARDIAN, 
                user_id=str(uuid.uuid4())),# testing if uuid4 is a valid id for user entity
            User(
                #presidente da dev
                name="Pedro", 
                email="20.00789-4@maua.br", 
                ra="20.00789-4", 
                state=STATE.APPROVED, 
                role=ROLE.PRESIDENT, 
                active=ACTIVE.ACTIVE, 
                course=COURSE.ECM, 
                year=5, 
                organization=ORGANIZATION.DEV, user_id="e6bed58f-424a-4b62-b408-18e0a8d1f069"),
            User(
                #estudante comum inativo (sem ser o admin do sistema)
                name="Lebron James", 
                email="15.01234-4@maua.br", 
                ra="15.01234-2",
                state=STATE.REJECTED, 
                role=ROLE.USER, 
                active=ACTIVE.DISCONNECTED, 
                course=COURSE.ECM, 
                year=5, 
                organization=ORGANIZATION.DEV, user_id="3d32ec27-09c3-41da-92e2-be106e449b6a")
        ]
        
    def get_dev_president(self) -> Optional[User]:
        
        for user in self.users:
            if user.organization == ORGANIZATION.DEV and user.role == ROLE.PRESIDENT:
                return user
            
    def get_nawat_president(self) -> Optional[User]:
        
        for user in self.users:
            if user.organization == ORGANIZATION.NAWAT and user.role == ROLE.PRESIDENT:
                return user
            
    def get_system_admin(self) -> Optional[User]:
        
        for user in self.users:
            if user.role == ROLE.ADM:
                return user
    
    def get_user(self, user_id: int) -> Optional[User]:
        for user in self.users:
            if user.user_id == user_id:
                return user
        raise NoItemsFound(user_id)
    
    def get_all_user(self) -> Optional[List[User]]:
        if not self.users:
            raise NoItemsFound("No users found")
        return self.users
    
    def create_user(self, new_user: User) -> Optional[User]:
        self.users.append(new_user)
        return new_user

    def delete_user(self, user_id: str) -> Optional[User]:
        for pos, user in enumerate(self.users):
            if user.user_id == user_id:
                self.users.pop(pos)
                return user
        raise NoItemsFound(user_id)

    def update_user(
        self, 
        user_id: str, 
        new_state: STATE =None, 
        new_role: ROLE =None, 
        new_active: ACTIVE=None, 
        new_course: COURSE=None, 
        new_year: int=None,  
        new_organization: ORGANIZATION=None
    ) -> Optional[User]:
        for user in self.users:
            if user.user_id == user_id:
                if new_state != None:
                    user.state= new_state
                if new_role != None:
                    user.role= new_role
                if new_active != None:
                    user.active= new_active
                if new_course != None:
                    user.course= new_course
                if new_year != None:
                    user.year= new_year
                if new_organization != None:
                    user.organization= new_organization
                return user
        raise NoItemsFound(user_id)
    
    def has_permission_target_user(self, requester_id: str, target_user: User) -> Optional[bool]:
        try:
            requester_user = self.get_user(user_id=requester_id)

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

        except NoItemsFound:
            raise NoItemsFound(requester_id)
        except ForbiddenAction as e:
            raise ForbiddenAction(e.message)
        
    def has_permission_target_id(self, requester_id: str, target_id: str) -> Optional[bool]:
        
        try:
            requester_user = self.get_user(user_id=requester_id)
            target_user = self.get_user(user_id=target_id)

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

        except NoItemsFound:
            raise NoItemsFound(requester_id)
        except ForbiddenAction as e:
            raise ForbiddenAction(e.message)

