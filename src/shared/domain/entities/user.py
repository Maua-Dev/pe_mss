import abc
import re
import uuid

from src.shared.domain.enums.active_enum import ACTIVE
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
    active: ACTIVE
    organization: ORGANIZATION
    MIN_NAME_LENGTH = 2
    user_id: str

    def __init__(
        self, 
        user_id: str,
        name: str,
        email: str,
        state: STATE, 
        role: ROLE, 
        active: ACTIVE,
        ra: str = None,        # essa linha deve existir pois existem emails maua sem ra, como por exemplo emails de professores
        course: COURSE=None,   #ou emails customizados, como o dev@maua.br. Muito provavelmente o email do Godoy nao é igual
        year: int=None,        #ao dos alunos que vamos conseguir extrair o ra direto.
        organization: ORGANIZATION=None, 
    ):
        if not User.validate_name(name):
            raise EntityError("name")
        self.name = name

        if not User.validate_email(email):
            raise EntityError("email")
        self.email = email

        if not User.validate_ra(ra) and ra is not None:
            raise EntityError("ra")
        self.ra = ra

        if type(state) != STATE:
            raise EntityError("state")
        self.state = state
        
        if type(role) != ROLE:
            raise EntityError("role")
        self.role = role
        
        if type(course) != COURSE and course is not None:
            raise EntityError("course")
        self.course = course

        if type(active) != ACTIVE:
            raise EntityError("active")
        self.active = active
        
        if not User.validate_year(year) and year is not None:
            raise EntityError("year")
        self.year = year

        if type(organization) != ORGANIZATION and organization is not None:
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

        if email[-8:] != "@maua.br":
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
        if type(year) != int:
            return False
        elif year < 0 or year > 5:
            return False
        
        return True

    @staticmethod
    def validate_id(user_id: str) -> bool:
        if type(user_id) != str:
            return False
        try:
            if uuid.UUID(user_id):
                return True
            
        except ValueError:
            raise InvalidUserIdFormat("Invalid format for user id")
        
    @classmethod
    def from_dict(cls, data: dict) -> "User":
        if 'state' in data and data['state'] is not None: data['state'] = STATE(data['state'])
        if 'role' in data and data['role'] is not None: data['role'] = ROLE(data['role'])
        if 'active' in data and data['active'] is not None: data['active'] = ACTIVE(data['active'])
        if 'course' in data and data['course'] is not None: data['course'] = COURSE(data['course'])
        if 'organization' in data and data['organization'] is not None: data['organization'] = ORGANIZATION(data['organization'])
        return cls(**data)

    def to_dict(self) -> dict:
        
        return {
            "user_id": self.user_id,
            "name": self.name,
            "ra": self.ra,
            "email": self.email,
            "course": self.course.value if self.course else None,
            "year": self.year,
            "role": self.role.value if self.role else None,
            "active": self.active.value if self.active else None,
            "organization": self.organization.value if self.organization else None,
            "state": self.state.value if self.state else None
        }

    def __repr__(self):
        return f"User(user_id={self.user_id}, name={self.name}, ra={self.ra}, email={self.email}, course={self.course.value if self.course else None}, year={self.year}, role={self.role.value if self.role else None}, active={self.active.value if self.active else None}, organization={self.organization.value if self.organization else None}, state={self.state.value if self.state else None})"

    def __eq__(self, other: "User"):
        if not isinstance(other, User):
            return False
        return (
            self.user_id == other.user_id,
            self.name == other.name,
            self.ra == other.ra,
            self.email == other.email,
            self.course == other.course,
            self.year == other.year,
            self.role == other.role,
            self.active == other.active,
            self.organization == other.organization,
            self.state == other.state
        )