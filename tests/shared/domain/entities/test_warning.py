from src.shared.domain.entities.warning import Warning, WarningBody
from pydantic import ValidationError
import datetime
import pytest

from src.shared.domain.enums.organization_enum import ORGANIZATION
from src.shared.domain.enums.role_enum import ROLE

class TestWarning:
    
    def test_warning(self):
        warning = Warning(
            target_role=ROLE.PRESIDENT,
            target_org=ORGANIZATION.DEV,
            body=WarningBody(
                title="Titulo do Aviso!",
                description="Descrição do Aviso!",
                expire=datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=7)
            ),
            created_at=datetime.datetime.now(datetime.timezone.utc)
        )
        
        assert warning.warning_id is not None
        assert ROLE(warning.target_role) == ROLE.PRESIDENT
        assert ORGANIZATION(warning.target_org) == ORGANIZATION.DEV
        assert warning.body.title == "Titulo do Aviso!"
        assert warning.body.description == "Descrição do Aviso!"
        assert warning.body.expire > datetime.datetime.now(datetime.timezone.utc)
        assert warning.created_at <= datetime.datetime.now(datetime.timezone.utc)
        
    def test_warning_wrong_type_title(self):
        with pytest.raises(ValidationError) as exc_info:
            Warning(
                target_role=ROLE.PRESIDENT,
                target_org=ORGANIZATION.DEV,
                body=WarningBody(
                    title=123,  # Tipo errado
                    description="Descrição do Aviso!",
                    expire=datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=7)
                ),
                created_at=datetime.datetime.now(datetime.timezone.utc)
            )
            
        assert "should be a valid string" in str(exc_info.value)
        
    def test_warning_missing_field(self):
        with pytest.raises(ValidationError) as exc_info:
            Warning(
                target_role=ROLE.PRESIDENT,
                target_org=ORGANIZATION.DEV,
                body=WarningBody(
                    # title ausente
                    description="Descrição do Aviso!",
                    expire=datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=7)
                ),
                created_at=datetime.datetime.now(datetime.timezone.utc)
            )
            
        assert "Field required" in str(exc_info.value)
        
    def test_warning_extra_field(self):
        with pytest.raises(ValidationError) as exc_info:
            Warning(
                target_role=ROLE.PRESIDENT,
                target_org=ORGANIZATION.DEV,
                body=WarningBody(
                    title="Titulo do Aviso!",
                    description="Descrição do Aviso!",
                    expire=datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=7)
                ),
                created_at=datetime.datetime.now(datetime.timezone.utc),
                extra_field="This field is not defined"  # Campo extra não definido
            )
            
        assert "Extra inputs are not permitted" in str(exc_info.value)
        
    def test_warning_invalid_enum(self):
        with pytest.raises(ValidationError) as exc_info:
            Warning(
                target_role="INVALID_ROLE",  # Valor inválido
                target_org=ORGANIZATION.DEV,
                body=WarningBody(
                    title="Titulo do Aviso!",
                    description="Descrição do Aviso!",
                    expire=datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=7)
                ),
                created_at=datetime.datetime.now(datetime.timezone.utc)
            )
            
        assert "Input should be 'ADM', 'USER' or 'PRESIDENT'" in str(exc_info.value)

        