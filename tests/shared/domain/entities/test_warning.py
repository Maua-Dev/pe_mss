from src.shared.domain.entities.warning import Warning
from pydantic import ValidationError
import datetime
import pytest

class TestWarning:
    
    def test_warning(self):
        
        now = datetime.datetime.now(datetime.UTC)
        
        warning = Warning(
            title="Titulo do Aviso",
            description="Descrição do Aviso!",
            expire=now, # agora no tempo UTC
            viewed=False
        )
        
        assert warning.title == "Titulo do Aviso"
        assert warning.description == "Descrição do Aviso!"
        assert warning.expire == now
        assert warning.viewed == False
        
    def test_warning_wrong_type_title(self):
        
        with pytest.raises(ValidationError) as exc_info:
            
            now = datetime.datetime.now(datetime.UTC)
            
            warning = Warning(
                title=123,
                description="Descrição do Aviso!",
                expire=now, # agora no tempo UTC
                viewed=False
            )
            
        errors = exc_info.value.errors()
        
        assert len(errors) == 1
        
        error_locations = {err['loc'][0] for err in errors}
        
        assert 'title' in error_locations
        
        title_error_message = next((err for err in errors if err['loc'][0] == 'title'), None)
        
        assert title_error_message.get("msg", None) == "Input should be a valid string"
        