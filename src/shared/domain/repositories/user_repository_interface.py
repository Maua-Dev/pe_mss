from abc import ABC, abstractmethod
from typing import List

from src.shared.domain.enums.course_enum import COURSE
from src.shared.domain.enums.organization_enum import ORGANIZATION
from src.shared.domain.enums.role_enum import ROLE
from src.shared.domain.enums.state_enum import STATE
from src.shared.domain.entities.user import User


class IUserRepository(ABC):

    @abstractmethod
    def get_user(self, user_id: int) -> User:
        """
        If user not found raise NoItemsFound
        """
        pass
        
    @abstractmethod
    def get_all_user(self) -> List[User]:
        """
        If no users found raise NoItemsFound"""
        pass

    @abstractmethod
    def create_user(self, new_user: User) -> User:
        """        
        Creates a new user and returns it
        """
        pass

    @abstractmethod
    def delete_user(self, user_id: str) -> User:
        """
        If user not found raise NoItemsFound
        """
        pass

    @abstractmethod
    def update_user(self, user_id: str, new_state: STATE=None, new_role: ROLE=None, new_course: COURSE=None, new_year: int=None,  new_organization: ORGANIZATION=None) -> User:
        """
        If user not found raise NoItemsFound
        """
        pass

    # @abstractmethod
    # def get_user_counter(self) -> int:
    #     """
    #     Returns the number of all users that have ever been created
    #     """
    #     pass

    @abstractmethod
    def check_if_requester_user_and_new_user_have_same_organization(self, id_user_requester : str, new_user :User) -> bool:
        """"
        Returns True if both users have the same organization, False otherwise
        """
        pass
