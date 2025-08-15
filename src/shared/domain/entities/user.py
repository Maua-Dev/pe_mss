import abc
import re
import uuid

from src.shared.domain.enums.course_enum import COURSE
from src.shared.domain.enums.organization_enum import ORGANIZATION
from src.shared.domain.enums.role_enum import ROLE
from src.shared.domain.enums.state_enum import STATE
from src.shared.helpers.errors.domain_errors import EntityError, InvalidUserIdFormat



class User(abc.ABC):
    name: str
    email: str
    ra: str
    state: STATE
    course: COURSE
    year: int
    role: ROLE
    organization: ORGANIZATION
    MIN_NAME_LENGTH = 2
    user_id: str

    def __init__(self, name: str, email: str, ra: str, state: STATE, course: COURSE, year: int, role: ROLE, organization: ORGANIZATION, user_id: str = None):
        if not User.validate_name(name):
            raise EntityError("name")
        self.name = name

        if not User.validate_email(email):
            raise EntityError("email")
        self.email = email

        if not User.validate_ra(ra):
            raise EntityError("ra")
        self.ra = ra

        if type(state) != STATE:
            raise EntityError("state")
        self.state = state

        if type(course) != COURSE:
            raise EntityError("course")
        self.course = course
        
        if not User.validate_year(year):
            raise EntityError("year")
        self.year = year

        if type(role) != ROLE:
            raise EntityError("role")
        self.role = role

        if type(organization) != ORGANIZATION:
            raise EntityError("entity")
        self.organization = organization

        if not User.validate_id(user_id):
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
    def validate_email(email: str) -> bool:
        if email is None:
            return False
        
        regex = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")

        return bool(re.fullmatch(regex, email))

    @staticmethod
    def validate_ra(ra: str) -> bool:
        if ra is None:
            return False
        elif type(ra) != str:
            return False
        
        ragex = re.compile(r"(^\d{2}\.?\d{5}-?\d{1}$)")

        return bool(re.fullmatch(ragex, ra))
    
    @staticmethod
    def validate_year(year: int) -> bool:
        if year is None:
            return False
        elif type(year) != int:
            return False
        elif year < 0 or year > 5:
            return False
        
        return True

    @staticmethod
    def validate_id(user_id: str) -> bool:
        if user_id is None:
            return False
        elif type(user_id) != str:
            return False
        try:
            if uuid.UUID(user_id):
                return True
            
        except ValueError:
            raise InvalidUserIdFormat("Invalid format for user id")
        
    def to_dict(self) -> dict:
        
        return {
            "user_id": self.user_id,
            "name": self.name,
            "ra": self.ra,
            "email": self.email,
            "course": self.course.value,
            "year": self.year,
            "role": self.role.value,
            "organization": self.organization.value,
            "state": self.state.value
        }

    def __repr__(self):
        return f"User(user_id={self.user_id}, name={self.name}, ra={self.ra}, email={self.email}, course={self.course.value}, year={self.year}, role={self.role}, organization={self.organization}, state={self.state})"

    def __eq__(self, other: "User"):
        return (
            self.user_id == other.user_id,
            self.name == other.name,
            self.ra == other.ra,
            self.email == other.email,
            self.course == other.course,
            self.year == other.year,
            self.role == other.role,
            self.organization == other.organization,
            self.state == other.state
        )