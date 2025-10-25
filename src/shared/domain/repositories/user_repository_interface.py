from abc import ABC, abstractmethod
from typing import List, Optional

from src.shared.domain.enums.active_enum import ACTIVE
from src.shared.domain.enums.course_enum import COURSE
from src.shared.domain.enums.organization_enum import ORGANIZATION
from src.shared.domain.enums.role_enum import ROLE
from src.shared.domain.enums.state_enum import STATE
from src.shared.domain.entities.user import User


class IUserRepository(ABC):

    @abstractmethod
    def get_user(self, user_id: str) -> Optional[User]:
        """
        If user not found raise NoItemsFound
        """
        pass

    @abstractmethod
    def get_user_by_email(self, email: str) -> Optional[User]:
        """
        If user not found raise NoItemsFound
        """
        pass
        
    @abstractmethod
    def get_all_user(self) -> Optional[List[Optional[User]]]:
        """
        If no users found raise NoItemsFound
        """
        pass

    @abstractmethod
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
        """
        Returns a list of users that match the given filters
        If no filters are provided, returns all users
        """
        pass

    @abstractmethod
    def create_user(self, new_user: User) -> Optional[User]:
        """        
        Creates a new user and returns it
        """
        pass

    @abstractmethod
    def delete_user(self, user_id: str) -> Optional[User]:
        """
        If user not found raise NoItemsFound
        """
        pass

    @abstractmethod
    def update_user(self, user_id: str, new_state: STATE=None, new_role: ROLE=None, new_active: ACTIVE=None, new_course: COURSE=None, new_year: int=None,  new_organization: ORGANIZATION=None) -> Optional[User]:
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
    def has_permission_target_user(self, requester_id : str, target_user :User) -> Optional[bool]:
        '''
        This method uses a target user, most likely will be used in create_user route!
        Returns True if user with requester id can perform actions onto target_id
        Evaluates Role and Organization
        If ( requester Role ends up being greater than target's AND requester is from same organization ) OR requester is simply admin: returns True
        Else will raise ForbiddenError or NoItemsFound
        '''
        pass
    
    @abstractmethod
    def has_permission_target_id(self, requester_id: str, target_id: str) -> Optional[bool]:
        '''
        This method uses a target id, most likely will be used in update, gets and delete routes!
        Returns True if user with requester id can perform actions onto target_id
        Evaluates Role and Organization
        If ( requester Role ends up being greater than target's AND requester is from same organization ) OR requester is simply admin: returns True
        Else will raise ForbiddenError or NoItemsFound
        '''
        pass
    
    @abstractmethod
    def reallocate_id(self, user_id: str, email: str) -> Optional[User]:
        """
        Changes the user_id of a user to the matching token id
        """
        pass