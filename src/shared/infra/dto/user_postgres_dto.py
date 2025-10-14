from src.shared.domain.entities.user import User
from src.shared.domain.enums.active_enum import ACTIVE
from src.shared.domain.enums.course_enum import COURSE
from src.shared.domain.enums.organization_enum import ORGANIZATION
from src.shared.domain.enums.role_enum import ROLE
from src.shared.domain.enums.state_enum import STATE


class UserPostgresDTO:
    user_id: str
    name: str
    email: str
    ra: str
    state: STATE
    course: COURSE
    year: int
    role: ROLE
    active: ACTIVE
    organization: ORGANIZATION


    def __init__(
            self,
            user_id: str,
            name: str,
            email: str,
            ra: str,
            state: STATE,
            course: COURSE,
            year: int,
            role: ROLE,
            active: ACTIVE,
            organization: ORGANIZATION
    ):
        self.user_id= user_id
        self.name= name
        self.email= email
        self.ra= ra
        self.role= role
        self.state= state
        self.active= active
        self.course= course
        self.year= year
        self.organization= organization

    
    @staticmethod
    def from_entity(user: User) -> "UserPostgresDTO":
        """
        Parse data from User to UserPostgresDTO
        """
        return UserPostgresDTO(
            user_id=user.user_id,
            name=user.name,
            email=user.email,
            ra=user.ra,
            role=user.role,
            state=user.state,
            active=user.active,
            course=user.course,
            year=user.year,
            organization=user.organization
        )
    
    def to_postgres(self) -> dict:
        """
        Parse data form UserPostgresDTO to dict
        """
        return {
            "user_id": self.user_id,
            "name": self.name,
            "email": self.email,
            "ra": self.ra if self.ra else None,
            "role": self.role.value,
            "state": self.state.value,
            "active": self.active.value,
            "course": self.course.value if self.course else None,
            "year": self.year if self.year else None,
            "organization": self.organization.value if self.organization else None
        }
    
    @staticmethod
    def from_postgres(user_data: dict) -> "UserPostgresDTO":
        """
        Parse data from Postgres to UserPostgresDTO
        @param user_data: dict from Postgres
        """
        return UserPostgresDTO(
            user_id=user_data["user_id"],
            name=user_data["name"],
            email=user_data["email"],
            ra=user_data["ra"] if "ra" in user_data else None,
            role=ROLE(user_data["role"]),
            state=STATE(user_data["state"]),
            active=ACTIVE(user_data["active"]),
            course=COURSE(user_data["course"]) if "course" in user_data else None,
            year=user_data["year"] if "year" in user_data else None,
            organization=ORGANIZATION(user_data["organization"]) if "organization" in user_data else None
        )
    
    def to_entity(self) -> User:
        """
        Parse data from UserPostgresDTO to User
        """
        return User(
            user_id= self.user_id,
            name= self.name,
            email= self.email,
            ra= self.ra,
            role= self.role,
            state= self.state,
            active= self.active,
            course= self.course,
            year= self.year,
            organization= self.organization
        )
    
    def __repr__(self):
        return f"UserPostgresDto(user_id={self.user_id}, name={self.name}, email={self.email}, ra={self.ra if self.ra else None}, role={self.role.value}, state={self.state.value}, active={self.active.value}, course={self.course.value if self.course else None}, year={self.year if self.year else None}, organization={self.organization.value if self.organization else None})"
    
    def __eq__(self, other: "UserPostgresDTO"):
        if not isinstance(other, UserPostgresDTO):
            return False
        return (
            self.user_id == other.user_id,
            self.name == other.name,
            self.email == other.email,
            self.ra == other.ra,
            self.role == other.role,
            self.state == other.state,
            self.active == other.active,
            self.course == other.course,
            self.year == other.year,
            self.organization == other.organization
        )
        