from src.shared.domain.entities.user import User
from src.shared.domain.enums.active_enum import ACTIVE
from src.shared.domain.enums.course_enum import COURSE
from src.shared.domain.enums.organization_enum import ORGANIZATION
from src.shared.domain.enums.role_enum import ROLE
from src.shared.domain.enums.state_enum import STATE


class UserPostgresDTO:
    user_id: str   #req
    name: str      #req
    email: str     #req
    ra: str        #req
    role: ROLE     #req
    state: STATE   #not req
    course: COURSE #not req
    year: int      #not req
    active: ACTIVE #not req
    organization: ORGANIZATION #not req


    def __init__(
            self,
            user_id: str,
            name: str,
            email: str,
            ra: str,
            role: ROLE,
            state: STATE | None,
            course: COURSE | None,
            year: int | None,
            active: ACTIVE | None,
            organization: ORGANIZATION | None
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
            "ra": self.ra,
            "role": self.role.value,
            "state": self.state.value if self.state else None,
            "active": self.active.value if self.active else None,
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
            user_id=user_data.get("user_id"),
            name=user_data.get("name"),
            email=user_data.get("email"),
            ra=user_data.get("ra"),
            role=ROLE(user_data.get("role")),
            state=STATE(user_data.get("state")) if user_data.get("state") is not None else None,
            active=ACTIVE(user_data.get("active")) if user_data.get("active") is not None else None,
            course=COURSE(user_data.get("course")) if user_data.get("course") is not None else None,
            year=user_data.get("year") if user_data.get("year") is not None else None,
            organization=ORGANIZATION(user_data.get("organization")) if user_data.get("organization") is not None else None
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
        