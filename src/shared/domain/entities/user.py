import abc
import re

from src.shared.domain.enums.state_enum import ENTITY, STATE, ROLE
from src.shared.helpers.errors.domain_errors import EntityError


class User(abc.ABC):
    name: str
    ra: str
    state: STATE
    course: str
    year: int
    role: ROLE
    entity: ENTITY
    MIN_NAME_LENGTH = 2
    user_id: int

    def __init__(self, name: str, ra: str, state: STATE, course: str, year: int, role: ROLE, entity: ENTITY, user_id: int = None):
        if not User.validate_name(name):
            raise EntityError("name")
        self.name = name

        if not User.validate_ra(ra):
            raise EntityError("ra")
        self.ra = ra

        if type(state) != STATE:
            raise EntityError("state")
        self.state = state

        if not User.validate_course(course):
            raise EntityError("course")
        self.course = course
        
        if not User.validate_year(year):
            raise EntityError("year")
        self.year = year

        if type(role) != ROLE:
            raise EntityError("role")
        self.role = role

        if type(entity) != ENTITY:
            raise EntityError("entity")
        self.entity = entity

        if type(user_id) == int:
            if user_id < 0:
                raise EntityError("user_id")
        if type(user_id) != int and user_id is not None:
            raise EntityError("user_id")

        self.user_id = user_id

    @staticmethod
    def validate_name(name: str) -> bool:
        if name is None:
            return False
        elif type(name) != str:
            return False
        elif len(name) < User.MIN_NAME_LENGTH:
            return False

        return True

    @staticmethod
    def validate_ra(ra: str) -> bool:
        if ra is None:
            return False
        elif type(ra) != str:
            return False
        
        ragex = re.compile(r"(^\d{2}\.?\d{5}-?\d{1}$)")

        return bool(re.fullmatch(ragex, ra))

    @staticmethod
    def validate_course(course: str) -> bool:
        if course is None:
            return False
        elif type(course) != str:
            return False
        
        return True
    
    @staticmethod
    def validate_year(year: int) -> bool:
        if year is None:
            return False
        elif type(year) != int:
            return False
        elif year < 0 or year > 5:
            return False
        
        return True

    def __repr__(self):
        return f"User(name={self.name}, ra={self.ra}, state={self.state}, course={self.course}, year={self.year}, role={self.role}, entity={self.entity}, user_id={self.user_id})"
