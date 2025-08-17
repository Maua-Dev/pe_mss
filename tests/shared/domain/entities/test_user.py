import uuid
from src.shared.domain.enums.course_enum import COURSE
from src.shared.domain.enums.organization_enum import ORGANIZATION
from src.shared.domain.enums.role_enum import ROLE
from src.shared.domain.entities.user import User
from src.shared.domain.enums.state_enum import STATE
from src.shared.helpers.errors.domain_errors import EntityError, InvalidUserIdFormat
import pytest


class Test_User:
    def test_user(self):
        User(name="VITOR", email="25.00178-5@maua.br", ra="25.00178-5", state=STATE.APPROVED, course=COURSE.CIC, year=1, role=ROLE.USER, organization=ORGANIZATION.DEV, user_id=f"{uuid.uuid4()}")

    def test_user_course_year_organization_are_none(self):
        User(name="VITOR", email="25.00178-5@maua.br", ra="25.00178-5", state=STATE.APPROVED, course=None, year=None, role=ROLE.USER, organization=None, user_id=f"{uuid.uuid4()}")

    def test_user_name_is_none(self):
        with pytest.raises(EntityError):
            User(name=None, email="25.00178-5@maua.br", ra="25.00178-5", state=STATE.APPROVED, course=COURSE.CIC, year=1, role=ROLE.USER, organization=ORGANIZATION.DEV, user_id=f"{uuid.uuid4()}")

    def test_user_name_is_not_str(self):
        with pytest.raises(EntityError):
            User(name=1, email="25.00178-5@maua.br", ra="25.00178-5", state=STATE.APPROVED, course=COURSE.CIC, year=1, role=ROLE.USER, organization=ORGANIZATION.DEV, user_id=f"{uuid.uuid4()}")

    def test_user_name_is_shorter_than_min_length(self):
        with pytest.raises(EntityError):
            User(name="V", email="25.00178-5@maua.br", ra="25.00178-5", state=STATE.APPROVED, course=COURSE.CIC, year=1, role=ROLE.USER, organization=ORGANIZATION.DEV, user_id=f"{uuid.uuid4()}")

    def test_user_email_is_none(self):
        with pytest.raises(EntityError):
            User(name="VITOR", email=None, ra="25.00178-5", state=STATE.APPROVED, course=COURSE.CIC, year=1, role=ROLE.USER, organization=ORGANIZATION.DEV, user_id=f"{uuid.uuid4()}")

    def test_user_email_is_not_valid(self):
        with pytest.raises(EntityError):
            User(name="VITOR", email="25.0178-5maua.br", ra="25.00178-5", state=STATE.APPROVED, course=COURSE.CIC, year=1, role=ROLE.USER, organization=ORGANIZATION.DEV, user_id=f"{uuid.uuid4()}")

    def test_user_ra_is_none(self):
        with pytest.raises(EntityError):
            User(name="VITOR", email="25.00178-5@maua.br",ra=None, state=STATE.APPROVED, course=COURSE.CIC, year=1, role=ROLE.USER, organization=ORGANIZATION.DEV, user_id=f"{uuid.uuid4()}")

    def test_user_ra_is_not_str(self):
        with pytest.raises(EntityError):
            User(name="VITOR", email="25.00178-5@maua.br",ra=25.00178-5, state=STATE.APPROVED, course=COURSE.CIC, year=1, role=ROLE.USER, organization=ORGANIZATION.DEV, user_id=f"{uuid.uuid4()}")

    def test_user_ra_is_not_valid(self):
        with pytest.raises(EntityError):
            User(name="VITOR", email="25.00178-5@maua.br", ra="254.00178-5", state=STATE.APPROVED, course=COURSE.CIC, year=1, role=ROLE.USER, organization=ORGANIZATION.DEV, user_id=f"{uuid.uuid4()}")

    def test_user_state_is_not_sate_enum(self):
        with pytest.raises(EntityError):
            User(name="VITOR", email="25.00178-5@maua.br", ra="25.00178-5", state="APPROVED", course=COURSE.CIC, year=1, role=ROLE.USER, organization=ORGANIZATION.DEV, user_id=f"{uuid.uuid4()}")

    def test_user_course_is_none(self):
        User(name="VITOR", email="25.00178-5@maua.br", ra="25.00178-5", state=STATE.APPROVED, course=None, year=1, role=ROLE.USER, organization=ORGANIZATION.DEV, user_id=f"{uuid.uuid4()}")

    def test_user_course_is_not_str(self):
        with pytest.raises(EntityError):
            User(name="VITOR", email="25.00178-5@maua.br", ra="25.00178-5", state=STATE.APPROVED, course=1, year=1, role=ROLE.USER, organization=ORGANIZATION.DEV, user_id=f"{uuid.uuid4()}")

    def test_user_year_is_none(self):
            User(name="VITOR", email="25.00178-5@maua.br", ra="25.00178-5", state=STATE.APPROVED, course=COURSE.CIC, year=None, role=ROLE.USER, organization=ORGANIZATION.DEV, user_id=f"{uuid.uuid4()}")

    def test_user_year_is_not_int(self):
        with pytest.raises(EntityError):
            User(name="VITOR", email="25.00178-5@maua.br", ra="25.00178-5", state=STATE.APPROVED, course=COURSE.CIC, year="1", role=ROLE.USER, organization=ORGANIZATION.DEV, user_id=f"{uuid.uuid4()}")

    def test_user_year_is_negative(self):
        with pytest.raises(EntityError):
            User(name="VITOR", email="25.00178-5@maua.br", ra="25.00178-5", state=STATE.APPROVED, course=COURSE.CIC, year=-1, role=ROLE.USER, organization=ORGANIZATION.DEV, user_id=f"{uuid.uuid4()}")

    def test_user_year_is_greater_than_five(self):
        with pytest.raises(EntityError):
            User(name="VITOR", email="25.00178-5@maua.br", ra="25.00178-5", state=STATE.APPROVED, course=COURSE.CIC, year=6, role=ROLE.USER, organization=ORGANIZATION.DEV, user_id=f"{uuid.uuid4()}")

    def test_user_role_is_not_role_enum(self):
        with pytest.raises(EntityError):
            User(name="VITOR", email="25.00178-5@maua.br", ra="25.00178-5", state=STATE.APPROVED, course=COURSE.CIC, year=1, role="USER", organization=ORGANIZATION.DEV, user_id=f"{uuid.uuid4()}")

    def test_user_organization_is_not_organization_enum(self):
        with pytest.raises(EntityError):
            User(name="VITOR", email="25.00178-5@maua.br", ra="25.00178-5", state=STATE.APPROVED, course=COURSE.CIC, year=1, role=ROLE.USER, organization="DEV", user_id=f"{uuid.uuid4()}")

    def test_user_organization_is_none(self):
        User(name="VITOR", email="25.00178-5@maua.br", ra="25.00178-5", state=STATE.APPROVED, course=COURSE.CIC, year=1, role=ROLE.USER, organization=None, user_id=f"{uuid.uuid4()}")

    def test_user_id_is_none(self):
        User(name="VITOR", email="25.00178-5@maua.br", ra="25.00178-5", state=STATE.APPROVED, course=COURSE.CIC,year=1, role=ROLE.USER, organization=ORGANIZATION.DEV, user_id=None)

    def test_user_user_id_is_not_a_string(self):
        with pytest.raises(EntityError):
            User(name="VITOR", email="25.00178-5@maua.br", ra="25.00178-5", state=STATE.APPROVED, course=COURSE.CIC, year=1, role=ROLE.USER, organization=ORGANIZATION.DEV, user_id=-1)

    def test_user_user_id_is_not_in_uuid_format(self):
        with pytest.raises(InvalidUserIdFormat):
            User(name="VITOR", email="25.00178-5@maua.br", ra="25.00178-5", state=STATE.APPROVED, course=COURSE.CIC, year=1, role=ROLE.USER, organization=ORGANIZATION.DEV, user_id="1")

    