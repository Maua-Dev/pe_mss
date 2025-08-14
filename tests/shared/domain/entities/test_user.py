from src.shared.domain.entities.user import User
from src.shared.domain.enums.state_enum import STATE, ROLE, ENTITY
from src.shared.helpers.errors.domain_errors import EntityError
import pytest


class Test_User:
    def test_user(self):
        User(name="VITOR", ra="25.00178-5", state=STATE.APPROVED, course="CIC", year=1, role=ROLE.USER, entity=ENTITY.DEV, user_id=1)

    def test_user_name_is_none(self):
        with pytest.raises(EntityError):
            User(name=None, ra="25.00178-5", state=STATE.APPROVED, course="CIC", year=1, role=ROLE.USER, entity=ENTITY.DEV, user_id=1)

    def test_user_name_is_not_str(self):
        with pytest.raises(EntityError):
            User(name=1, ra="25.00178-5", state=STATE.APPROVED, course="CIC", year=1, role=ROLE.USER, entity=ENTITY.DEV, user_id=1)

    def test_user_name_is_shorter_than_min_length(self):
        with pytest.raises(EntityError):
            User(name="V", ra="25.00178-5", state=STATE.APPROVED, course="CIC", year=1, role=ROLE.USER, entity=ENTITY.DEV, user_id=1)

    def test_user_ra_is_none(self):
        with pytest.raises(EntityError):
            User(name="VITOR",ra=None, state=STATE.APPROVED, course="CIC", year=1, role=ROLE.USER, entity=ENTITY.DEV, user_id=1)

    def test_user_ra_is_not_str(self):
        with pytest.raises(EntityError):
            User(name="VITOR", ra=25.00178-5, state=STATE.APPROVED, course="CIC", year=1, role=ROLE.USER, entity=ENTITY.DEV, user_id=1)

    def test_user_ra_is_not_valid(self):
        with pytest.raises(EntityError):
            User(name="VITOR", ra="254.00178-5", state=STATE.APPROVED, course="CIC", year=1, role=ROLE.USER, entity=ENTITY.DEV, user_id=1)

    def test_user_state_is_not_sate_enum(self):
        with pytest.raises(EntityError):
            User(name="VITOR", ra="25.00178-5", state="APPROVED", course="CIC", year=1, role=ROLE.USER, entity=ENTITY.DEV, user_id=1)

    def test_user_course_is_none(self):
        with pytest.raises(EntityError):
            User(name="VITOR", ra="25.00178-5", state=STATE.APPROVED, course=None, year=1, role=ROLE.USER, entity=ENTITY.DEV, user_id=1)

    def test_user_course_is_not_str(self):
        with pytest.raises(EntityError):
            User(name="VITOR", ra="25.00178-5", state=STATE.APPROVED, course=1, year=1, role=ROLE.USER, entity=ENTITY.DEV, user_id=1)

    def test_user_year_is_none(self):
        with pytest.raises(EntityError):
            User(name="VITOR", ra="25.00178-5", state=STATE.APPROVED, course="CIC", year=None, role=ROLE.USER, entity=ENTITY.DEV, user_id=1)

    def test_user_year_is_not_int(self):
        with pytest.raises(EntityError):
            User(name="VITOR", ra="25.00178-5", state=STATE.APPROVED, course="CIC", year="1", role=ROLE.USER, entity=ENTITY.DEV, user_id=1)

    def test_user_year_is_negative(self):
        with pytest.raises(EntityError):
            User(name="VITOR", ra="25.00178-5", state=STATE.APPROVED, course="CIC", year=-1, role=ROLE.USER, entity=ENTITY.DEV, user_id=1)

    def test_user_year_is_greater_than_five(self):
        with pytest.raises(EntityError):
            User(name="VITOR", ra="25.00178-5", state=STATE.APPROVED, course="CIC", year=6, role=ROLE.USER, entity=ENTITY.DEV, user_id=1)

    def test_user_role_is_not_role_enum(self):
        with pytest.raises(EntityError):
            User(name="VITOR", ra="25.00178-5", state=STATE.APPROVED, course="CIC", year=1, role="USER", entity=ENTITY.DEV, user_id=1)

    def test_user_entity_is_not_entity_enum(self):
        with pytest.raises(EntityError):
            User(name="VITOR", ra="25.00178-5", state=STATE.APPROVED, course="CIC", year=1, role=ROLE.USER, entity="DEV", user_id=1)

    def test_user_user_id_is_not_int(self):
        with pytest.raises(EntityError):
            User(name="VITOR", ra="25.00178-5", state=STATE.APPROVED, course="CIC", year=1, role=ROLE.USER, entity=ENTITY.DEV, user_id="1")

    def test_user_user_id_is_negative(self):
        with pytest.raises(EntityError):
            User(name="VITOR", ra="25.00178-5", state=STATE.APPROVED, course="CIC", year=1, role=ROLE.USER, entity=ENTITY.DEV, user_id=-1)